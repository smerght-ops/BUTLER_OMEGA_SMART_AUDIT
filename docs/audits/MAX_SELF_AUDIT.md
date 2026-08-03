# MAX SELF AUDIT — Butler

Generated UTC: `2026-07-07T22:44:11.103387Z`

## Built artifacts

- ✅ `Inspector0_PhysicalMap.json` — schema: `physical_map`, generator: `Inspector0_PhysicalMap`
- ✅ `Inspector1_EntityMap.json` — schema: `entity_map`, generator: `Inspector1_EntityMap`
- ✅ `Inspector2_ImportMap.json` — schema: `import_map`, generator: `Inspector2_ImportMap`
- ✅ `Inspector3_RegistrationAST.json` — schema: `registration_ast`, generator: `Inspector3_RegistrationAST`
- ✅ `Inspector4_CallGraph.json` — schema: `call_graph`, generator: `Inspector4_CallGraph`
- ✅ `LinkMap.json` — schema: `link_map`, generator: `LinkMapBuilder`
- ✅ `DependencyModel.json` — schema: `dependency_model`, generator: `DependencyModelBuilder`

## DependencyModel summary

- **nodes**: `1499`
- **edges**: `11976`
- **relations**: `{'import': 1528, 'call': 10428, 'registration': 20}`
- **orphan_nodes**: `0`
- **root_nodes**: `457`
- **leaf_nodes**: `1042`

## Role index

- **unclassified**: `1207` files
- **report**: `33` files
- **analyzer**: `119` files
- **inspector**: `16` files
- **builder**: `30` files
- **passport**: `38` files
- **memory**: `146` files
- **runner**: `61` files
- **dispatcher**: `40` files
- **registry**: `35` files
- **manager**: `151` files
- **guardian**: `65` files
- **policy**: `6` files
- **semantic**: `32` files

## Findings

- **info** `DUPLICATE_FILENAMES`: 115

## Lock recommendation

Do not rebuild existing measurement pipeline artifacts unless schema/version is intentionally changed.
