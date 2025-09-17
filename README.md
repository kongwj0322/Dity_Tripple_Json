# Dity_Tripple_Json

## TBM Collapse Mechanism Data

This repository contains hierarchical mechanism-oriented JSON data for TBM (Tunnel Boring Machine) collapse risk analysis. The system transforms direct causal relationships into detailed multi-hop mechanism chains to better understand the pathways that lead to tunnel collapse.

### Data Files

- **data/raw_input.json** - Original raw triples data containing direct causal relationships to TBM tunnel collapse
- **data/TBM_collapse_mechanism_full.json** - Generated hierarchical mechanism JSON with expanded causal chains
- **scripts/build_mechanism_json.py** - Reproducible script that transforms raw input into hierarchical mechanisms

### Field Schema

Each edge in the JSON follows this schema:
- `subject`: The source node (risk factor, event, or condition)
- `parent_subject_type`: Parent type classification (typically "RiskFactor")
- `subject_type`: Type of the subject (Equipment&Tools, Methods&Params, Event, HydroFactors, GeologyCondition, etc.)
- `weight`: Numeric weight as string (e.g., "0.8008")
- `prior_probability`: Prior probability value (typically "0")
- `predicate`: Relationship type ("导致" for causation, "触发" for triggers)
- `object`: The target node
- `object_type`: Type of the object (Event, Methods&Params, CollapseType, RiskResult, etc.)
- `relation_type`: Relation classification ("因果关系" for causal relationships)

### Transformation Rules

The system applies these transformation rules to convert direct causal edges:

1. **Equipment/Tools Failures**: Main bearing damage, cutterhead issues, screw conveyor blockages, etc. are transformed into chains involving parameter anomalies → pressure differentials → face instability → collapse
2. **Methods & Parameters**: Injection parameters, mud properties, advancing speed issues are converted into chains through intermediate mechanism states
3. **Hydro/Geological Factors**: Water and geological conditions are expanded through stability degradation pathways
4. **Support Structure Issues**: Support inadequacies are chained through structural failure mechanisms

### Weight Policy

- First hop in each mechanism chain preserves the original weight from raw input
- Subsequent hops decrease by 0.0001 per hop (e.g., 0.8008 → 0.8007 → 0.8006...)
- Weights are bounded between 0.7500 and 0.8500
- Missing weights default to "0.8000"

### Node Types

- **Event**: Intermediate process states (e.g., "掌子面失稳", "土体流失")
- **Methods&Params**: Construction parameters (e.g., "土压不足", "仓压差异常")
- **CollapseType**: Specific collapse mechanisms (e.g., "掌子面坍塌", "洞身段塌方")
- **RiskResult**: Final outcome ("TBM隧道塌方")
- **HydroFactors**: Water-related factors (e.g., "孔隙水压力升高")

### Regenerating the Data

To regenerate the hierarchical mechanism JSON:

```bash
python3 scripts/build_mechanism_json.py
```

This reads `data/raw_input.json` and generates `data/TBM_collapse_mechanism_full.json` with expanded mechanism chains replacing direct causal edges to "TBM隧道塌方".