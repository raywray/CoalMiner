"""
These functions take in some user provided parameters and randomly determine an evolutionary history to output to a .tpl file
"""

import random
import re


def write_tpl(
    filename,
    number_of_populations,
    population_effective_sizes,
    sample_sizes,
    growth_rates,
    migration_matrices,
    historical_events,
):
    # flatten the nested list
    flattened_migration_matrices = []
    for matrix in migration_matrices:
        for line in matrix:
            flattened_migration_matrices.append(line)
    lines = [
        "//Number of population samples (demes)",
        str(number_of_populations),
        "//Population effective sizes (number of genes)",
        *population_effective_sizes,
        "//Sample Sizes",
        *[str(size) for size in sample_sizes],
        "//Growth rates : negative growth implies population expansion",
        *[str(size) for size in growth_rates],
        "//Number of migration matrices : 0 implies no migration between demes",
        str(len(migration_matrices)),
        *flattened_migration_matrices,
        "//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index",
        f"{len(historical_events)} historical event",
        *historical_events,
        "//Number of independent loci [chromosome]",
        "1 0",
        "//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci",
        "1",
        "//per Block:data type, number of loci, per gen recomb and mut rates",
        f"FREQ 1 0 MUTRATE$ OUTEXP",
        "",
    ]

    # write to file
    with open(filename, "w") as tpl_file:
        tpl_file.writelines("\n".join(lines))


def get_population_list(num_pops, ghost_present):
    # this function returns the population names
    populations = []
    population_range = num_pops - 1 if ghost_present else num_pops

    for i in range(0, population_range):
        populations.append(str(i))

    if ghost_present:
        populations.append("G")
    return populations


def get_population_effective_sizes(number_of_populations, ghost_present):
    return [
        f"N_POP{i}$" for i in get_population_list(number_of_populations, ghost_present)
    ]


def get_admix_sources_and_sinks(ghost_present, number_of_populations):
    # define nested functions
    def add_source_or_sink(possible_sources_or_sinks):
        sources_or_sinks = []
        # iterate through all populations
        for _ in range(random.randint(1, number_of_populations)):
            if possible_sources_or_sinks == []:
                break  # no more possibilities
            new_source_or_sink = random.choice(
                possible_sources_or_sinks
            )  # pick a source/sink from possibilites
            sources_or_sinks.append(str(new_source_or_sink))  # add to respective list
            possible_sources_or_sinks.remove(
                new_source_or_sink
            )  # remove from possibilites
        return sources_or_sinks

    # initialize empty lists
    sources, sinks = [], []

    # randomly assign populations to sources or sinks (not all populations need be included)
    while sources == sinks:  # keep iterating until sources and sinks are not identical
        # add all populations as a possibility
        possible_sources = list(range(number_of_populations))
        possible_sinks = list(range(number_of_populations))

        if ghost_present:
            possible_sources.pop(
                -1
            )  # delete the last possible pop (so that we can assign it as "G" later)
            possible_sinks.pop(-1)

            # determine if ghost is source or sink
            if random.choice([True, False]):
                possible_sources.append("G")
            else:
                possible_sinks.append("G")

        # randomly choose sources & sinks
        sources.extend(add_source_or_sink(possible_sources))
        sinks.extend(add_source_or_sink(possible_sinks))

    return sources, sinks


def get_divergence_events(ghost_present, number_of_populations, pops_should_migrate):
    # define nested functions
    def get_deme(source_or_sink):
        # check to see if the source ro sink is a ghost
        if str(source_or_sink) == "G":
            # if so, return the correct population number
            return str(number_of_populations - 1)
        else:
            # if not, just return a string of the input
            return str(source_or_sink)

    # start by defining empty list
    divergence_events = []
    # define all populations as nodes
    nodes = list(range(number_of_populations))

    # if ghost present, will replace its index with "G"
    if ghost_present:
        nodes.pop(-1)

    # randomly determine how many sinks
    number_of_sinks = (
        random.choice(range(1, number_of_populations))
        if ghost_present
        else random.choice(range(1, number_of_populations + 1))
    )
    # assign pops as sinks
    sinks = random.sample(nodes, number_of_sinks)
    # assign all other pops as sources (can be 0)
    sources = [node for node in nodes if node not in sinks]

    # finish randomly assigning ghost as a source or sink if ghost exists
    if ghost_present:
        if random.choice([True, False]):
            sources.append("G")
        else:
            sinks.append("G")

    # the first divergence event should be in mig mat 1
    current_migration_matrix = 1 if pops_should_migrate else 0

    # iterate as long as there are sources, or at least 2 sinks (the sinks will act as sources as soon as the sources are gone)
    while sources or len(sinks) > 1:
        # define empty event
        current_event = []
        # randomly select a source
        cur_source = random.choice(sources) if sources else random.choice(sinks)
        # remove the selected source from the sources list
        sources.remove(cur_source) if sources else sinks.remove(cur_source)
        # randomly select a sink
        cur_sink = random.choice(sinks)
        # randomly choose whether to resize the new deme or not (a deme size of "0" would result in extinction)
        new_deme_size = random.choice([f"RELANC{cur_source}{cur_sink}$", "1"])
        # add params to current event
        current_event.extend(
            [
                f"T_DIV{cur_source}{cur_sink}$",
                get_deme(cur_source),
                get_deme(cur_sink),
                "1",  # migrants
                new_deme_size,
                "0",  # growth rate
                str(current_migration_matrix),
            ]
        )
        # add event to divergence events
        divergence_events.append(" ".join(current_event))
        # only increment migration matrix index if there should be migration
        if pops_should_migrate:
            current_migration_matrix += 1

    return divergence_events


def get_admixture_events(ghost_present, num_pops):
    # get potential sources and sinks for the admixture event
    sources, sinks = get_admix_sources_and_sinks(ghost_present, num_pops)

    # randomly select admixture/migration percentage
    migrants = random.uniform(0, 1)

    # select two unique populations
    unique_source_and_sink = False
    while not unique_source_and_sink:
        source = random.choice(sources)
        sink = random.choice(sinks)

        if source != sink:
            unique_source_and_sink = True

    # initialize empty admixture event list
    admixture_events = []
    # create current event
    current_event = [
        f"T_ADMIX{source}{sink}$",
        str(num_pops) if source == "G" else source,
        str(num_pops) if sink == "G" else sink,
        str(migrants),
        "1",  # new deme size, "1" implies that the size of the sink deme remains unchanged
        "0",  # growth rate
        "0",  # migration matrix
    ]
    admixture_events.append(" ".join(current_event))  # add to all admixture events

    return admixture_events


def get_bottleneck_events(num_pops, ghost_present):
    # initialize empty list for bottleneck events
    bottleneck_events = []

    # find the pop to bottleneck
    source = sink = str(random.choice(list(range(num_pops))))
    if ghost_present:
        if source == str(num_pops - 1):
            source = sink = "G"

    # define bottleneck start
    current_event = [
        f"T_BOT{source}{sink}$",
        str(num_pops - 1) if source == "G" else str(source),
        str(num_pops - 1) if sink == "G" else str(sink),
        "0",  # migrants
        f"RESBOT{source}{sink}$",  # new deme size
        "0",  # growth rate
        "0",  # migration matrix
    ]

    bottleneck_events.append(" ".join(current_event))

    return bottleneck_events


def order_historical_events(historical_events):
    # define nested functions
    def extract_source_sink(event):
        m = re.search(r"T_(?:DIV|ADMIX|BOT)(G|\d+)(G|\d+)\$", event)
        if not m:
            return None, None
        return m.group(1), m.group(2)

    def is_migration_switch_event(event):
        """Check if event is a migration-switching event (has no source/sink)"""
        return any(
            event.startswith(prefix)
            for prefix in ["T_MIGSTOP", "T_CONTACT", "T_PULSE_START", "T_PULSE_END"]
        )

    def place_events(current_ordered_events, events_to_add):
        # make a copy
        newly_ordered_events = current_ordered_events.copy()

        # iterate through new events
        for cur_event in events_to_add:
            # extract the current source and sink
            cur_source, cur_sink = extract_source_sink(cur_event)

            # Skip events where source/sink cannot be extracted
            if cur_source is None or cur_sink is None:
                continue

            # Start with all possible insertion points, including "append at end"
            possible_insertion_indices = list(range(len(newly_ordered_events) + 1))

            # loop through current ordered events (use the updated list)
            for i, event in enumerate(newly_ordered_events):
                event_source, _ = extract_source_sink(event)

                # stop once the current event's source/sink would be "dead"
                # forbid inserting AFTER this point
                if cur_source == event_source or cur_sink == event_source:
                    possible_insertion_indices = possible_insertion_indices[: i + 1]
                    break

            # If no valid positions, insert at beginning (should be rare)
            insertion_index = random.choice(possible_insertion_indices) if possible_insertion_indices else 0
            newly_ordered_events.insert(insertion_index, cur_event)

        return newly_ordered_events

    def add_end_events(current_ordered_events, event_type):
        # make a copy
        robust_ordered_events = current_ordered_events.copy()
        for event in current_ordered_events:
            # select the pertinenet event type
            if event.startswith(f"T_{event_type}"):
                event_parts = event.split()
                # create the "end" event
                end_event = (
                    event_parts[0].replace(f"T_{event_type}", f"T_{event_type}END")
                    + " "
                    + " ".join(event_parts[1:])
                )
                # replace the event start deme resize with the event end deme resize
                end_resize = event_parts[4].replace(
                    f"RES{event_type}", f"RES{event_type}END"
                )
                end_event = end_event.replace(event_parts[4], end_resize)

                event_index = robust_ordered_events.index(event)
                robust_ordered_events.insert(
                    event_index + 1, end_event
                )  # add to all events right after the starting event
        return robust_ordered_events

    ordered_historical_events = []
    # divide events into event types
    admix_events = []
    bot_events = []
    mig_switch_events = []

    for event in historical_events:
        if "T_DIV" in event:
            # add div events to ordered bc they are already in order
            ordered_historical_events.append(event)
        elif "T_ADMIX" in event:
            admix_events.append(event)
        elif "T_BOT" in event:
            bot_events.append(event)
        elif is_migration_switch_event(event):
            # migration switching events (no source/sink)
            mig_switch_events.append(event)
        # TODO: add other events here

    # put events in random -- but chronologically correct -- order
    # start with admixture events
    ordered_historical_events = place_events(ordered_historical_events, admix_events)
    # then, bottleneck events
    if bot_events:
        ordered_historical_events = place_events(ordered_historical_events, bot_events)
        # here, make sure that the bottleneck endings are accurate
        ordered_historical_events = add_end_events(ordered_historical_events, "BOT")

    # insert migration switching events at random valid positions
    # (they don't have source/sink constraints)
    for mig_event in mig_switch_events:
        if ordered_historical_events:
            # Insert at a random position among existing events
            insertion_index = random.randint(0, len(ordered_historical_events))
            ordered_historical_events.insert(insertion_index, mig_event)
        else:
            ordered_historical_events.append(mig_event)

    return ordered_historical_events


def get_historical_events(ghost_present, number_of_populations, pops_should_migrate):
    """
    This function generates all historical events - divergence, admixture, and bottlenecks
    """

    # initalize empty list
    historical_events = []

    # get divergence events
    divergence_events = get_divergence_events(
        ghost_present=ghost_present,
        number_of_populations=number_of_populations,
        pops_should_migrate=pops_should_migrate,
    )
    historical_events.extend(
        divergence_events
    )  # add divergence events to historical events

    # randomize adding admixture (50% probability)
    if random.choice([True, False]):
        admixture_events = get_admixture_events(
            ghost_present=ghost_present, num_pops=number_of_populations
        )
        historical_events.extend(
            admixture_events
        )  # add admixture events to historical events

    # randomize adding bottlenecks (50% probability)
    if random.choice([True, False]):
        bottleneck_events = get_bottleneck_events(number_of_populations, ghost_present)
        historical_events.extend(bottleneck_events)

    # TODO: add exponential growths.

    # place historical events in chronological order
    historical_events = order_historical_events(
        historical_events=historical_events,
    )

    return historical_events, divergence_events


def get_matrix_template(
    num_pops, ghost_present, matrix_index=0, migration_varies_by_matrix=False
):
    # this function filles out a completed migration matrix (i.e. migration between all pops)
    matrix_label = f"//Migration matrix {matrix_index}"
    matrix = [matrix_label]

    for i in range(1, num_pops + 1):
        row = []
        for j in range(1, num_pops + 1):
            if i == j:
                matrix_i_j = "0.000"
            else:
                populations_list = get_population_list(num_pops, ghost_present)
                from_pop = populations_list[i - 1]
                to_pop = populations_list[j - 1]
                # Add matrix index suffix if migration varies by matrix
                if migration_varies_by_matrix:
                    matrix_i_j = f"MIG{from_pop}{to_pop}_{matrix_index}$"
                else:
                    matrix_i_j = f"MIG{from_pop}{to_pop}$"
            row.append(matrix_i_j)
        matrix.append(" ".join(row))
    return matrix


def get_migration_matrices(
    num_pops, ghost_present, divergence_events, migration_varies_by_matrix=False
):
    # define in nested functions
    def extract_coalescing_population(event):
        m = re.search(r"^T_DIV(G|\d+)(G|\d+)\$", event.split()[0])
        if not m:
            return None
        src = m.group(1)
        if ghost_present and src == str(num_pops - 1):
            return "G"
        return src

    # start by defining empty list
    matrices = []
    # the first matrix is a complete migration matrix
    first_matrix = get_matrix_template(
        num_pops,
        ghost_present,
        matrix_index=0,
        migration_varies_by_matrix=migration_varies_by_matrix,
    )
    matrices.append(first_matrix)

    # start with the fully filled out migration matrix
    current_matrix = get_matrix_template(
        num_pops,
        ghost_present,
        matrix_index=0,
        migration_varies_by_matrix=migration_varies_by_matrix,
    )

    # Track all populations that have coalesced (for varying migration option)
    coalesced_populations = []

    # loop through all divergence events going back in time
    for i in range(len(divergence_events)):
        current_event = divergence_events[i]
        # find the migration matrix of the current event
        current_event_matrix_index = int(re.search(r"\d+$", current_event).group())

        # If migration varies by matrix, create a new template for this matrix
        # Otherwise, use the current matrix and remove coalesced populations
        if migration_varies_by_matrix:
            current_matrix = get_matrix_template(
                num_pops,
                ghost_present,
                matrix_index=current_event_matrix_index,
                migration_varies_by_matrix=True,
            )

            # Zero out migration for all previously coalesced populations
            matrix_without_label = current_matrix[1:]
            for coalesced_pop in coalesced_populations:
                pattern = r"MIG{}[0-9a-zA-Z]*_\d+\$|MIG[0-9a-zA-Z]*{}_\d+\$".format(
                    coalesced_pop, coalesced_pop
                )
                matrix_without_label = [
                    re.sub(pattern, "0.000", line) for line in matrix_without_label
                ]
            current_matrix = [current_matrix[0]] + matrix_without_label

        # get the coalescing population (the source)
        coalescing_population = extract_coalescing_population(current_event)

        # Track this population as coalesced for future matrices (varying migration only)
        if migration_varies_by_matrix and coalescing_population:
            coalesced_populations.append(coalescing_population)

        # Pattern to match migration parameters with the coalescing population
        # Need to handle both with and without matrix index suffix
        if migration_varies_by_matrix:
            coalescing_population_in_matrix_pattern = (
                r"MIG{}[0-9a-zA-Z]*_\d+\$|MIG[0-9a-zA-Z]*{}_\d+\$".format(
                    coalescing_population, coalescing_population
                )
            )
        else:
            coalescing_population_in_matrix_pattern = (
                r"MIG{}[0-9a-zA-Z$]*|MIG[0-9a-zA-Z]*{}\$".format(
                    coalescing_population, coalescing_population
                )
            )

        # make a temp matrix without the label
        matrix_without_label = current_matrix[1:]

        # replace any MIG param that has the coalescing population in i
        current_matrix = [
            re.sub(coalescing_population_in_matrix_pattern, "0.000", line)
            for line in matrix_without_label
        ]
        # get updated matrix label
        matrix_label = f"//Migration matrix {current_event_matrix_index}"

        # add label to new matrix
        current_matrix.insert(0, matrix_label)

        # add to the matrices list
        matrices.append(current_matrix)

    return matrices


def choose_migration_family():
    """
    Choose one migration family from the available options using weighted random selection.

    Returns:
        str: One of "IM_THEN_ISO", "SECONDARY_CONTACT", "CONSTANT_MIG", "PULSE"
    """
    families = ["IM_THEN_ISO", "SECONDARY_CONTACT", "CONSTANT_MIG", "PULSE"]
    weights = [0.4, 0.3, 0.2, 0.1]

    # Use random.choices for weighted selection (Python 3.6+)
    return random.choices(families, weights=weights, k=1)[0]


def apply_migration_family_to_event_indices(ordered_events, family):
    """
    Rewrite migration matrix indices (last field) in ordered events to be consistent
    with the chosen migration family. This prevents events from incorrectly "turning
    migration back on" after a switch event due to random ordering.

    ordered_events: List of event strings ordered most recent -> oldest
    family: Migration family name

    Returns:
        List of rewritten event strings
    """

    def set_last_field(event, idx):
        """Helper to set the last field (migration matrix index) of an event"""
        parts = event.split()
        if len(parts) >= 7:
            parts[-1] = str(idx)
        return " ".join(parts)

    # For PULSE family, ensure T_PULSE_START comes before T_PULSE_END
    events = ordered_events.copy()
    if family == "PULSE":
        start_idx = None
        end_idx = None
        for i, event in enumerate(events):
            if event.startswith("T_PULSE_START"):
                start_idx = i
            elif event.startswith("T_PULSE_END"):
                end_idx = i

        # If END appears before START (more recent), swap them
        if start_idx is not None and end_idx is not None and end_idx < start_idx:
            events[start_idx], events[end_idx] = events[end_idx], events[start_idx]

    # Initialize current migration matrix index
    # PULSE starts at 0 (no migration), others start at 0 (migration if applicable)
    current_idx = 0

    rewritten_events = []

    for event in events:
        # Handle migration-switching events that change the current epoch
        if event.startswith("T_MIGSTOP") or event.startswith("T_CONTACT"):
            # Switch from migration (0) to no migration (1) going backward in time
            current_idx = 1
            rewritten_events.append(set_last_field(event, 1))

        elif event.startswith("T_PULSE_START"):
            # Enter pulse window (start migration) going backward
            current_idx = 1
            rewritten_events.append(set_last_field(event, 1))

        elif event.startswith("T_PULSE_END"):
            # Exit pulse window (end migration) going backward
            current_idx = 2
            rewritten_events.append(set_last_field(event, 2))

        else:
            # Regular event (DIV, ADMIX, BOT, etc.) - use current epoch's index
            # This prevents the event from overriding the migration regime
            rewritten_events.append(set_last_field(event, current_idx))

    return rewritten_events


def get_migration_matrices_optionA(
    num_pops, ghost_present, divergence_events, family, migration_varies_by_matrix=False
):
    """
    Build migration matrices based on the chosen migration family.

    Args:
        num_pops: Number of populations
        ghost_present: Whether ghost population exists
        divergence_events: List of divergence event strings
        family: Migration family ("IM_THEN_ISO", "SECONDARY_CONTACT", "CONSTANT_MIG", "PULSE")
        migration_varies_by_matrix: Whether migration parameters vary by matrix

    Returns:
        List of migration matrices
    """
    matrices = []

    if family == "CONSTANT_MIG":
        # Only matrix 0 with full migration
        matrix = get_matrix_template(
            num_pops,
            ghost_present,
            matrix_index=0,
            migration_varies_by_matrix=migration_varies_by_matrix,
        )
        matrices.append(matrix)

    elif family == "IM_THEN_ISO":
        # Matrix 0: full migration (recent)
        # Matrix 1: no migration (old)
        matrix_0 = get_matrix_template(
            num_pops,
            ghost_present,
            matrix_index=0,
            migration_varies_by_matrix=migration_varies_by_matrix,
        )
        matrices.append(matrix_0)

        # Matrix 1: all zeros
        matrix_1_label = "//Migration matrix 1"
        matrix_1 = [matrix_1_label]
        for i in range(1, num_pops + 1):
            row = ["0.000"] * num_pops
            matrix_1.append(" ".join(row))
        matrices.append(matrix_1)

    elif family == "SECONDARY_CONTACT":
        # Matrix 0: full migration (recent)
        # Matrix 1: no migration (old)
        # Same structure as IM_THEN_ISO, different conceptual interpretation
        matrix_0 = get_matrix_template(
            num_pops,
            ghost_present,
            matrix_index=0,
            migration_varies_by_matrix=migration_varies_by_matrix,
        )
        matrices.append(matrix_0)

        # Matrix 1: all zeros
        matrix_1_label = "//Migration matrix 1"
        matrix_1 = [matrix_1_label]
        for i in range(1, num_pops + 1):
            row = ["0.000"] * num_pops
            matrix_1.append(" ".join(row))
        matrices.append(matrix_1)

    elif family == "PULSE":
        # Matrix 0: no migration (most recent)
        # Matrix 1: full migration (pulse window)
        # Matrix 2: no migration (old)

        # Matrix 0: all zeros
        matrix_0_label = "//Migration matrix 0"
        matrix_0 = [matrix_0_label]
        for i in range(1, num_pops + 1):
            row = ["0.000"] * num_pops
            matrix_0.append(" ".join(row))
        matrices.append(matrix_0)

        # Matrix 1: full migration
        matrix_1 = get_matrix_template(
            num_pops,
            ghost_present,
            matrix_index=1,
            migration_varies_by_matrix=migration_varies_by_matrix,
        )
        matrices.append(matrix_1)

        # Matrix 2: all zeros
        matrix_2_label = "//Migration matrix 2"
        matrix_2 = [matrix_2_label]
        for i in range(1, num_pops + 1):
            row = ["0.000"] * num_pops
            matrix_2.append(" ".join(row))
        matrices.append(matrix_2)

    return matrices


def generate_random_params(
    tpl_filename, user_given_number_of_populations, user_given_sample_sizes
):
    # determine if there is a ghost population
    add_ghost = random.choice([True, False])

    # Determine total number of populations -- either given by user or + 1 if there is a ghost pop)
    number_of_populations = (
        user_given_number_of_populations + 1
        if add_ghost
        else user_given_number_of_populations
    )

    # determine sample sizes -- user-provided and add 0 if there is a ghost population
    sample_sizes = (
        user_given_sample_sizes + [0] if add_ghost else user_given_sample_sizes
    )

    # set inital growth rates to 0
    initial_growth_rates = [0] * number_of_populations

    # determine if there should be migration (50% probability)
    pops_should_migrate = random.choice([True, False])

    # if there is migration, determine if migration rates vary by matrix (50% probability)
    migration_varies_by_matrix = False
    if pops_should_migrate:
        migration_varies_by_matrix = random.choice([True, False])

    # generate historical events
    historical_events, divergence_events = get_historical_events(
        ghost_present=add_ghost,
        number_of_populations=number_of_populations,
        pops_should_migrate=pops_should_migrate,
    )

    # build migration matrices (if there is migration)
    if pops_should_migrate:
        # Choose migration family
        migration_family = choose_migration_family()

        # Add migration-switching events based on family
        if migration_family == "IM_THEN_ISO":
            mig_stop_event = "T_MIGSTOP$ -1 -1 0 1 0 1"
            historical_events.append(mig_stop_event)

        elif migration_family == "SECONDARY_CONTACT":
            contact_event = "T_CONTACT$ -1 -1 0 1 0 1"
            historical_events.append(contact_event)

        elif migration_family == "PULSE":
            pulse_start_event = "T_PULSE_START$ -1 -1 0 1 0 1"
            pulse_end_event = "T_PULSE_END$ -1 -1 0 1 0 2"
            historical_events.append(pulse_start_event)
            historical_events.append(pulse_end_event)

        # CONSTANT_MIG: no switch events needed

        # Order all historical events (including migration switches)
        historical_events = order_historical_events(historical_events)

        # Rewrite migration matrix indices to be consistent with the chosen family
        # This must happen AFTER ordering to prevent events from overriding
        # the migration regime when randomly placed
        historical_events = apply_migration_family_to_event_indices(
            historical_events, migration_family
        )

        # Recompute divergence_events from the rewritten historical events
        # for use in matrix generation
        divergence_events = [e for e in historical_events if e.startswith("T_DIV")]

        # Build migration matrices using the new approach
        migration_matrices = get_migration_matrices_optionA(
            num_pops=number_of_populations,
            ghost_present=add_ghost,
            divergence_events=divergence_events,
            family=migration_family,
            migration_varies_by_matrix=migration_varies_by_matrix,
        )
    else:
        migration_matrices = []

    # assign population effective size variable names
    population_effective_sizes = get_population_effective_sizes(
        number_of_populations, add_ghost
    )

    # write all generated parameters and variables to a tpl file
    write_tpl(
        filename=tpl_filename,
        number_of_populations=number_of_populations,
        population_effective_sizes=population_effective_sizes,
        sample_sizes=sample_sizes,
        growth_rates=initial_growth_rates,
        migration_matrices=migration_matrices,
        historical_events=historical_events,
    )


def test_migration_families():
    """
    Internal test function to validate migration family implementation.
    Generates 20 models and checks for consistency.
    """
    print("Testing migration family implementation...")
    print("=" * 60)

    import tempfile
    import os

    for i in range(20):
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tpl", delete=False) as f:
            temp_filename = f.name

        try:
            # Generate random model
            generate_random_params(
                tpl_filename=temp_filename,
                user_given_number_of_populations=random.randint(2, 4),
                user_given_sample_sizes=[20] * random.randint(2, 4),
            )

            # Read and validate the file
            with open(temp_filename, "r") as f:
                content = f.read()

            # Extract migration matrix count
            lines = content.split("\n")
            for idx, line in enumerate(lines):
                if line.startswith("//Number of migration matrices"):
                    num_matrices = int(lines[idx + 1])
                    break
            else:
                num_matrices = 0

            # Extract max referenced matrix index from historical events
            max_matrix_idx = -1
            in_events_section = False
            event_indices = []  # Track indices in order for validation
            for line in lines:
                if "historical event:" in line:
                    in_events_section = True
                    continue
                if in_events_section and line.strip() and not line.startswith("//"):
                    parts = line.split()
                    if len(parts) >= 7:
                        try:
                            matrix_idx = int(parts[-1])
                            max_matrix_idx = max(max_matrix_idx, matrix_idx)
                            event_indices.append(matrix_idx)
                        except (ValueError, IndexError):
                            pass
                if line.startswith("//Number of independent loci"):
                    break

            # Determine family based on content
            family = "UNKNOWN"
            if "T_MIGSTOP" in content:
                family = "IM_THEN_ISO"
            elif "T_CONTACT" in content:
                family = "SECONDARY_CONTACT"
            elif "T_PULSE_START" in content:
                family = "PULSE"
            elif num_matrices == 1:
                family = "CONSTANT_MIG"
            elif num_matrices == 0:
                family = "NO_MIGRATION"

            # Validate matrix count
            if num_matrices > 0:
                assert (
                    max_matrix_idx < num_matrices
                ), f"Model {i}: Max matrix index {max_matrix_idx} >= num matrices {num_matrices}"

            # Family-specific validation of event indices
            if family == "IM_THEN_ISO" or family == "SECONDARY_CONTACT":
                # After first occurrence of 1, no later event should have 0
                if 1 in event_indices:
                    first_one_idx = event_indices.index(1)
                    for idx in event_indices[first_one_idx + 1 :]:
                        assert (
                            idx != 0
                        ), f"Model {i} ({family}): Found index 0 after index 1: {event_indices}"

            elif family == "PULSE":
                # Indices should be non-decreasing and subset of {0,1,2}
                for idx in event_indices:
                    assert idx in [
                        0,
                        1,
                        2,
                    ], f"Model {i} (PULSE): Invalid index {idx}, expected 0, 1, or 2"
                # Check non-decreasing (allowing repeats)
                for j in range(len(event_indices) - 1):
                    assert (
                        event_indices[j] <= event_indices[j + 1]
                    ), f"Model {i} (PULSE): Indices not non-decreasing: {event_indices}"

            elif family == "CONSTANT_MIG":
                # All indices should be 0
                for idx in event_indices:
                    assert (
                        idx == 0
                    ), f"Model {i} (CONSTANT_MIG): Expected all indices to be 0, found {idx}"

            print(
                f"Model {i+1:2d}: {family:20s} | matrices: {num_matrices} | max_idx: {max_matrix_idx} | indices: {event_indices if event_indices else 'none'}"
            )

        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

    print("=" * 60)
    print("All tests passed!")
