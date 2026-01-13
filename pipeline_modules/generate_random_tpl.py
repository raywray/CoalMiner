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
        match = re.search(r"T*([0-9G]{2})", event)
        source, sink = match.group(1)
        return source, sink

    def place_events(current_ordered_events, events_to_add):
        # make a copy
        newly_ordered_events = current_ordered_events.copy()
        # iterate through new events
        for cur_event in events_to_add:
            # extract the current source and sink
            cur_source, cur_sink = extract_source_sink(cur_event)

            # initilalize list of possible places to insert admix event
            possible_insertion_indeces = []

            # loop through current ordered events
            for event in current_ordered_events:
                event_source, event_sink = extract_source_sink(event)

                # add the index of the event to possible indeces
                possible_insertion_indeces.append(current_ordered_events.index(event))

                # check to see if either cur event sink or source is dead
                if cur_source == event_source or cur_sink == event_source:
                    break

            insertion_index = random.choice(possible_insertion_indeces)
            newly_ordered_events.insert(insertion_index, cur_event)
            newly_ordered_events = set_migration_matrix(
                newly_ordered_events, insertion_index
            )

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

    for event in historical_events:
        if "T_DIV" in event:
            # add div events to ordered bc they are already in order
            ordered_historical_events.append(event)
        elif "T_ADMIX" in event:
            admix_events.append(event)
        elif "T_BOT" in event:
            bot_events.append(event)
        # TODO: add other events here

    # put events in random -- but chronologically correct -- order
    # start with admixture events
    ordered_historical_events = place_events(ordered_historical_events, admix_events)
    # then, bottleneck events
    if bot_events:
        ordered_historical_events = place_events(ordered_historical_events, bot_events)
        # here, make sure that the bottleneck endings are accurate
        ordered_historical_events = add_end_events(ordered_historical_events, "BOT")

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


def set_migration_matrix(events, event_index):
    current_event = events[event_index]
    possible_mig_mat_indeces = []

    previous_event = events[event_index - 1] if event_index != 0 else None
    next_event = events[event_index + 1] if event_index != len(events) - 1 else None

    migration_matrix_extraction_pattern = r"(\d+)$"
    prev_match = (
        re.search(migration_matrix_extraction_pattern, previous_event)
        if previous_event
        else None
    )
    next_match = (
        re.search(migration_matrix_extraction_pattern, next_event)
        if next_event
        else None
    )

    possible_mig_mat_indeces = [prev_match.group(1)] if prev_match else ["0"]
    if next_match:
        possible_mig_mat_indeces.append(next_match.group(1))

    new_migration_matrix = random.choice(possible_mig_mat_indeces)
    updated_current_event = re.sub(
        migration_matrix_extraction_pattern, new_migration_matrix, current_event
    )

    events[event_index] = updated_current_event

    return events


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
        # find the coalescing pop (the source)
        match = re.search(r"^T_DIV([0-9a-zA-Z])+[0-9a-zA-Z]", event)
        if match:
            coalescing_population = match.group(1)
            # if ghost, replace number with "G"
            if ghost_present:
                if coalescing_population == str(num_pops - 1):
                    return "G"
            return coalescing_population
        else:
            return None

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
        migration_matrices = get_migration_matrices(
            num_pops=number_of_populations,
            ghost_present=add_ghost,
            divergence_events=divergence_events,
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
