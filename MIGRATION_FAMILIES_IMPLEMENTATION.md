# Migration Families Implementation

## Overview
The code now supports four distinct migration families instead of the previous "monotonically shutting off" behavior. Each model randomly selects one family using weighted probabilities.

**Branch**: `raya/mig-mat-current`  
**Modified file**: `pipeline_modules/generate_random_tpl.py`

## Bug Fix (Latest Update)

**Issue**: Migration matrix indices were being forced before event ordering, causing inconsistent behavior where events could "turn migration back on/off" incorrectly after random insertion of migration-switching events.

**Solution**: Implemented `apply_migration_family_to_event_indices()` that rewrites all event indices AFTER ordering, ensuring consistency with the chosen migration family throughout time. This prevents events from overriding the migration regime.

**Key Changes**:
- Removed pre-forcing of indices before ordering
- Added post-ordering pass to rewrite indices consistently
- Fixed PULSE ordering to ensure T_PULSE_START comes before T_PULSE_END
- Added comprehensive validation in tests

## Migration Families

### 1. CONSTANT_MIG (weight: 0.2)
- **Description**: Migration remains constant throughout the model's history
- **Matrices**: 1 matrix (matrix 0) with full migration parameters
- **Events**: All divergence events reference matrix index 0
- **Backward-time interpretation**: Migration present from present to deepest past

### 2. IM_THEN_ISO (weight: 0.4)
- **Description**: Isolation with Migration, then Isolation
- **Matrices**: 
  - Matrix 0: Full migration (recent epoch)
  - Matrix 1: No migration (older epoch)
- **Events**: 
  - Divergence events use matrix 0
  - One `T_MIGSTOP$` event switches to matrix 1
- **Backward-time interpretation**: Recent past has migration, older past is isolated

### 3. SECONDARY_CONTACT (weight: 0.3)
- **Description**: Recent contact after historical isolation
- **Matrices**: 
  - Matrix 0: Full migration (recent epoch)
  - Matrix 1: No migration (older epoch)
- **Events**: 
  - Divergence events use matrix 0
  - One `T_CONTACT$` event switches to matrix 1
- **Backward-time interpretation**: Same structure as IM_THEN_ISO, different conceptual framing

### 4. PULSE (weight: 0.1)
- **Description**: A window of migration sandwiched between periods of isolation
- **Matrices**:
  - Matrix 0: No migration (most recent)
  - Matrix 1: Full migration (pulse window)
  - Matrix 2: No migration (oldest)
- **Events**:
  - Divergence events use matrix 0
  - `T_PULSE_START$` switches to matrix 1 (entering pulse)
  - `T_PULSE_END$` switches to matrix 2 (exiting pulse)
- **Backward-time interpretation**: No migration present → migration window → no migration in deep past

## Key Implementation Details

### Functions Added

#### `choose_migration_family()`
Returns one of the four families using weighted random selection.

#### `get_migration_matrices_optionA()`
Builds migration matrices appropriate for the chosen family:
- Takes parameters: `num_pops`, `ghost_present`, `divergence_events`, `family`, `migration_varies_by_matrix`
- Returns list of migration matrices in fastsimcoal2 format

#### Updated `order_historical_events()`
Now handles migration-switching events (T_MIGSTOP, T_CONTACT, T_PULSE_START, T_PULSE_END) which:
- Don't have source/sink pairs
- Can be inserted at random valid positions
- Don't violate chronological constraints

### Modified `generate_random_params()`
When migration is enabled:
1. Chooses a migration family
2. Adjusts all divergence events to reference valid matrix indices
3. Adds family-specific migration-switching events
4. Re-orders all historical events
5. Builds matrices using `get_migration_matrices_optionA()`

## Validation

The `test_migration_families()` function generates 20 random models and validates:
- Files write without errors
- Number of matrices matches expected for each family
- Historical events only reference existing matrix indices
- All four families appear in output

## Example Outputs

### CONSTANT_MIG Example
```
//Number of migration matrices : 0 implies no migration between demes
1
//Migration matrix 0
0.000 MIG01$ MIG02$
MIG10$ 0.000 MIG12$
MIG20$ MIG21$ 0.000
```

### IM_THEN_ISO Example
```
//Number of migration matrices : 0 implies no migration between demes
2
//Migration matrix 0
0.000 MIG01$ MIG02$
MIG10$ 0.000 MIG12$
MIG20$ MIG21$ 0.000
//Migration matrix 1
0.000 0.000 0.000
0.000 0.000 0.000
0.000 0.000 0.000
//historical event: ...
T_MIGSTOP$ -1 -1 0 1 0 1
```

### PULSE Example
```
//Number of migration matrices : 0 implies no migration between demes
3
//Migration matrix 0
0.000 0.000 0.000
0.000 0.000 0.000
0.000 0.000 0.000
//Migration matrix 1
0.000 MIG01$ MIG02$
MIG10$ 0.000 MIG12$
MIG20$ MIG21$ 0.000
//Migration matrix 2
0.000 0.000 0.000
0.000 0.000 0.000
0.000 0.000 0.000
//historical event: ...
T_PULSE_START$ -1 -1 0 1 0 1
T_PULSE_END$ -1 -1 0 1 0 2
```

## Ghost Population Support

All migration families correctly handle ghost populations by:
- Using "G" suffix in migration parameter names (e.g., `MIG0G$`, `MIGG1$`)
- Preserving ghost logic through `get_matrix_template()`

## Compatibility

- Output format is fully compatible with `write_tpl()`
- Integration with existing est file generation (`generate_random_est.py`)
- Supports `migration_varies_by_matrix` parameter for all families
