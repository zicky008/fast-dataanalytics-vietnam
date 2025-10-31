"""
Semantic Layer Implementation - Adapted from WrenAI MDL
Production-ready with full Pydantic validation
₫0 cost, 100% Python, Enterprise-grade quality
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional, Literal, Any
import yaml
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# ===== PYDANTIC MODELS (Same structure as WrenAI) =====

class Column(BaseModel):
    """Column definition with type validation"""
    name: str
    type: str  # STRING, INTEGER, FLOAT, DATE, BOOLEAN, TIMESTAMP
    isCalculated: bool = False
    expression: Optional[str] = None
    description: Optional[str] = None
    isHidden: bool = False
    
    @field_validator('type')
    @classmethod
    def validate_type(cls, v):
        valid_types = ['STRING', 'INTEGER', 'FLOAT', 'DATE', 'BOOLEAN', 'TIMESTAMP']
        if v.upper() not in valid_types:
            raise ValueError(f"Type must be one of {valid_types}, got '{v}'")
        return v.upper()
    
    def to_ddl(self) -> str:
        """Generate DDL fragment for this column"""
        ddl = f"{self.name} {self.type}"
        if self.description:
            ddl += f" -- {self.description}"
        return ddl


class Measure(BaseModel):
    """Metric measure definition"""
    name: str
    type: Literal['MEASURE', 'CALCULATED_MEASURE']
    operator: Optional[Literal['SUM', 'COUNT', 'AVG', 'MAX', 'MIN']] = None
    expression: str
    description: Optional[str] = None
    
    @field_validator('expression')
    @classmethod
    def validate_expression(cls, v):
        if not v or not v.strip():
            raise ValueError("Expression cannot be empty")
        return v.strip()


class TimeGrain(BaseModel):
    """Time dimension for metrics"""
    name: str
    refColumn: str
    dateParts: List[Literal['YEAR', 'QUARTER', 'MONTH', 'WEEK', 'DAY']]
    
    @field_validator('dateParts')
    @classmethod
    def validate_date_parts(cls, v):
        if not v:
            raise ValueError("dateParts cannot be empty")
        return v


class Metric(BaseModel):
    """Pre-defined metric with dimensions and measures"""
    name: str
    baseObject: str  # Reference to model name
    dimension: List[str] = []
    measure: List[Measure]
    timeGrain: List[TimeGrain] = []
    description: Optional[str] = None
    benchmark: Optional[str] = None  # Industry benchmark for reference
    
    @field_validator('measure')
    @classmethod
    def validate_measures(cls, v):
        if not v:
            raise ValueError("Metric must have at least one measure")
        return v


class Model(BaseModel):
    """Data model (table) definition"""
    name: str
    tableReference: str  # File path or table name
    columns: List[Column]
    primaryKey: str
    cached: bool = False
    description: Optional[str] = None
    
    @field_validator('primaryKey')
    @classmethod
    def validate_primary_key(cls, v, info):
        # Validate that primaryKey exists in columns
        columns = info.data.get('columns', [])
        column_names = [col.name for col in columns]
        if v not in column_names:
            raise ValueError(
                f"Primary key '{v}' not found in columns. "
                f"Available columns: {', '.join(column_names)}"
            )
        return v
    
    @field_validator('columns')
    @classmethod
    def validate_columns(cls, v):
        if not v:
            raise ValueError("Model must have at least one column")
        
        # Check for duplicate column names
        names = [col.name for col in v]
        duplicates = [name for name in names if names.count(name) > 1]
        if duplicates:
            raise ValueError(f"Duplicate column names found: {set(duplicates)}")
        
        return v
    
    def get_column(self, name: str) -> Optional[Column]:
        """Get column by name"""
        for col in self.columns:
            if col.name == name:
                return col
        return None
    
    def to_ddl(self) -> str:
        """Generate CREATE TABLE DDL"""
        lines = [f"CREATE TABLE {self.name} ("]
        for i, col in enumerate(self.columns):
            if col.isHidden:
                continue
            comma = "," if i < len(self.columns) - 1 else ""
            lines.append(f"  {col.to_ddl()}{comma}")
        lines.append(f"  PRIMARY KEY ({self.primaryKey})")
        lines.append(");")
        
        if self.description:
            lines.append(f"-- {self.description}")
        
        return "\n".join(lines)


class Relationship(BaseModel):
    """Relationship between two models"""
    name: str
    models: List[str]  # Must have exactly 2 models
    joinType: Literal['ONE_TO_ONE', 'ONE_TO_MANY', 'MANY_TO_ONE', 'MANY_TO_MANY']
    condition: str  # e.g., "tickets.agent_id = agents.agent_id"
    description: Optional[str] = None
    
    @field_validator('models')
    @classmethod
    def validate_models(cls, v):
        if len(v) != 2:
            raise ValueError(f"Relationship must have exactly 2 models, got {len(v)}: {v}")
        if v[0] == v[1]:
            raise ValueError(f"Cannot create relationship between same model: {v[0]}")
        return v
    
    @field_validator('condition')
    @classmethod
    def validate_condition(cls, v, info):
        if not v or not v.strip():
            raise ValueError("Relationship condition cannot be empty")
        
        # Basic validation: should contain '=' and both model names
        models = info.data.get('models', [])
        if '=' not in v:
            raise ValueError(f"Condition must contain '=' for JOIN: {v}")
        
        # Check that both models are referenced
        for model in models:
            if model not in v:
                logger.warning(
                    f"Model '{model}' not found in condition '{v}'. "
                    f"This may cause JOIN errors."
                )
        
        return v.strip()
    
    def to_sql(self) -> str:
        """Generate SQL JOIN fragment"""
        join_type_map = {
            'ONE_TO_ONE': 'INNER JOIN',
            'ONE_TO_MANY': 'LEFT JOIN',
            'MANY_TO_ONE': 'INNER JOIN',
            'MANY_TO_MANY': 'FULL OUTER JOIN',
        }
        join_sql = join_type_map.get(self.joinType, 'INNER JOIN')
        return f"{join_sql} {self.models[1]} ON {self.condition}"


class SemanticLayer(BaseModel):
    """Complete Semantic Layer (MDL) - Matches WrenAI structure"""
    catalog: str
    schema_name: str = Field(alias="schema")
    dataSource: Literal['LOCAL_FILE', 'POSTGRES', 'MYSQL', 'BIGQUERY', 'SNOWFLAKE', 'DUCKDB']
    models: List[Model]
    relationships: List[Relationship] = []
    metrics: List[Metric] = []
    version: str = "1.0"
    
    class Config:
        populate_by_name = True
    
    @field_validator('models')
    @classmethod
    def validate_models(cls, v):
        if not v:
            raise ValueError("Semantic layer must have at least one model")
        
        # Check for duplicate model names
        names = [model.name for model in v]
        duplicates = [name for name in names if names.count(name) > 1]
        if duplicates:
            raise ValueError(f"Duplicate model names found: {set(duplicates)}")
        
        return v
    
    @field_validator('relationships')
    @classmethod
    def validate_relationships(cls, v, info):
        models = info.data.get('models', [])
        model_names = {model.name for model in models}
        
        for rel in v:
            for model_ref in rel.models:
                if model_ref not in model_names:
                    raise ValueError(
                        f"Relationship '{rel.name}' references unknown model '{model_ref}'. "
                        f"Available models: {', '.join(model_names)}"
                    )
        
        return v
    
    @field_validator('metrics')
    @classmethod
    def validate_metrics(cls, v, info):
        models = info.data.get('models', [])
        model_names = {model.name for model in models}
        
        for metric in v:
            if metric.baseObject not in model_names:
                raise ValueError(
                    f"Metric '{metric.name}' references unknown base object '{metric.baseObject}'. "
                    f"Available models: {', '.join(model_names)}"
                )
        
        return v


# ===== SEMANTIC LAYER PARSER =====

class SemanticLayerParser:
    """
    Production-ready semantic layer parser
    Validates MDL schema and provides intelligent query routing
    
    Usage:
        parser = SemanticLayerParser("domain.mdl.yaml")
        mdl = parser.load()
        context = parser.generate_context("What's our FCR rate?")
    """
    
    def __init__(self, mdl_path: str):
        self.mdl_path = Path(mdl_path)
        self.semantic_layer: Optional[SemanticLayer] = None
        
        # Fast lookup indexes
        self.models_by_name: Dict[str, Model] = {}
        self.metrics_by_name: Dict[str, Metric] = {}
        self.relationships_map: Dict[str, List[Relationship]] = {}
        
        # Search index for columns
        self.column_index: Dict[str, List[tuple[str, Column]]] = {}
    
    def load(self) -> SemanticLayer:
        """Load and validate MDL from YAML"""
        if not self.mdl_path.exists():
            raise FileNotFoundError(f"MDL file not found: {self.mdl_path}")
        
        logger.info(f"Loading semantic layer from: {self.mdl_path}")
        
        with open(self.mdl_path, 'r', encoding='utf-8') as f:
            raw_data = yaml.safe_load(f)
        
        # Validate with Pydantic (catches all schema errors)
        try:
            self.semantic_layer = SemanticLayer(**raw_data)
        except Exception as e:
            logger.error(f"MDL validation failed: {e}")
            raise
        
        # Build lookup indexes for fast query routing
        self._build_indexes()
        
        logger.info(f"✅ Loaded semantic layer: {self.semantic_layer.catalog}")
        logger.info(f"   Models: {len(self.semantic_layer.models)}")
        logger.info(f"   Relationships: {len(self.semantic_layer.relationships)}")
        logger.info(f"   Metrics: {len(self.semantic_layer.metrics)}")
        
        return self.semantic_layer
    
    def _build_indexes(self):
        """Build fast lookup indexes for O(1) access"""
        # Index models
        for model in self.semantic_layer.models:
            self.models_by_name[model.name] = model
            
            # Index columns for search
            for col in model.columns:
                col_lower = col.name.lower()
                if col_lower not in self.column_index:
                    self.column_index[col_lower] = []
                self.column_index[col_lower].append((model.name, col))
        
        # Index metrics
        for metric in self.semantic_layer.metrics:
            self.metrics_by_name[metric.name] = metric
        
        # Index relationships by model
        for rel in self.semantic_layer.relationships:
            for model_name in rel.models:
                if model_name not in self.relationships_map:
                    self.relationships_map[model_name] = []
                self.relationships_map[model_name].append(rel)
    
    def get_model(self, name: str) -> Optional[Model]:
        """Get model by name (O(1) lookup)"""
        return self.models_by_name.get(name)
    
    def get_metric(self, name: str) -> Optional[Metric]:
        """Get metric by name (O(1) lookup)"""
        return self.metrics_by_name.get(name)
    
    def get_related_models(self, model_name: str) -> List[tuple[str, Relationship]]:
        """Get all models related to given model"""
        relationships = self.relationships_map.get(model_name, [])
        related = []
        for rel in relationships:
            other_model = [m for m in rel.models if m != model_name][0]
            related.append((other_model, rel))
        return related
    
    def find_columns(self, query: str) -> List[tuple[str, Column]]:
        """Find columns mentioned in query (case-insensitive)"""
        query_lower = query.lower()
        matches = []
        
        for col_name, col_list in self.column_index.items():
            if col_name in query_lower:
                matches.extend(col_list)
        
        return matches
    
    def find_metrics(self, query: str) -> List[Metric]:
        """Find metrics mentioned in query"""
        query_lower = query.lower()
        matches = []
        
        for metric in self.semantic_layer.metrics:
            # Match by metric name
            if metric.name.lower() in query_lower:
                matches.append(metric)
                continue
            
            # Match by measure names
            for measure in metric.measure:
                if measure.name.lower() in query_lower:
                    matches.append(metric)
                    break
            
            # Match by description keywords
            if metric.description and any(
                word in metric.description.lower() 
                for word in query_lower.split()
            ):
                matches.append(metric)
        
        return matches
    
    def find_models(self, query: str) -> List[Model]:
        """Find models relevant to query"""
        query_lower = query.lower()
        matches = []
        
        for model in self.semantic_layer.models:
            # Match by model name
            if model.name.lower() in query_lower:
                matches.append(model)
                continue
            
            # Match by description
            if model.description and model.description.lower() in query_lower:
                matches.append(model)
        
        return matches
    
    def generate_context(self, query: str, max_models: int = 5) -> str:
        """
        Generate LLM context based on query
        Returns formatted context with relevant models, metrics, relationships
        """
        context_parts = []
        
        # Find relevant components
        mentioned_columns = self.find_columns(query)
        relevant_models = set(model_name for model_name, _ in mentioned_columns)
        mentioned_metrics = self.find_metrics(query)
        
        # If no specific mentions, include top models by relevance
        if not relevant_models:
            relevant_models = set(
                model.name for model in self.find_models(query)[:max_models]
            )
        
        # Build context
        if relevant_models:
            context_parts.append("### RELEVANT DATA MODELS ###")
            for model_name in list(relevant_models)[:max_models]:
                model = self.get_model(model_name)
                if not model:
                    continue
                
                context_parts.append(f"\n**Model: {model.name}**")
                context_parts.append(f"Source: {model.tableReference}")
                
                if model.description:
                    context_parts.append(f"Description: {model.description}")
                
                context_parts.append("Columns:")
                for col in model.columns:
                    if col.isHidden:
                        continue
                    col_info = f"  - {col.name} ({col.type})"
                    if col.description:
                        col_info += f": {col.description}"
                    if col.isCalculated:
                        col_info += f" [Calculated: {col.expression}]"
                    context_parts.append(col_info)
                
                # Add related models
                related = self.get_related_models(model_name)
                if related:
                    context_parts.append("Related to:")
                    for other_model, rel in related:
                        context_parts.append(
                            f"  - {other_model} ({rel.joinType}): {rel.condition}"
                        )
        
        if mentioned_metrics:
            context_parts.append("\n### RELEVANT METRICS ###")
            for metric in mentioned_metrics:
                context_parts.append(f"\n**Metric: {metric.name}**")
                context_parts.append(f"Base Object: {metric.baseObject}")
                
                if metric.description:
                    context_parts.append(f"Description: {metric.description}")
                
                if metric.benchmark:
                    context_parts.append(f"Industry Benchmark: {metric.benchmark}")
                
                context_parts.append("Measures:")
                for measure in metric.measure:
                    measure_info = f"  - {measure.name}: {measure.expression}"
                    if measure.description:
                        measure_info += f" ({measure.description})"
                    context_parts.append(measure_info)
                
                if metric.dimension:
                    context_parts.append(f"Dimensions: {', '.join(metric.dimension)}")
        
        # Add data source info
        context_parts.append("\n### DATA SOURCE ###")
        context_parts.append(f"Type: {self.semantic_layer.dataSource}")
        context_parts.append(f"Catalog: {self.semantic_layer.catalog}")
        context_parts.append(f"Schema: {self.semantic_layer.schema_name}")
        
        return "\n".join(context_parts)
    
    def to_dict(self) -> dict:
        """Export to dictionary (for JSON serialization)"""
        if not self.semantic_layer:
            raise ValueError("No semantic layer loaded")
        return self.semantic_layer.model_dump(by_alias=True)
    
    def validate(self) -> Dict[str, Any]:
        """Validate semantic layer and return validation report"""
        if not self.semantic_layer:
            raise ValueError("No semantic layer loaded")
        
        report = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "stats": {
                "models": len(self.semantic_layer.models),
                "relationships": len(self.semantic_layer.relationships),
                "metrics": len(self.semantic_layer.metrics),
                "columns": sum(len(m.columns) for m in self.semantic_layer.models),
            }
        }
        
        # Check for orphaned relationships
        for rel in self.semantic_layer.relationships:
            for model_name in rel.models:
                if model_name not in self.models_by_name:
                    report["errors"].append(
                        f"Relationship '{rel.name}' references unknown model '{model_name}'"
                    )
                    report["valid"] = False
        
        # Check for metrics without measures
        for metric in self.semantic_layer.metrics:
            if not metric.measure:
                report["warnings"].append(
                    f"Metric '{metric.name}' has no measures defined"
                )
        
        # Check for models without primary keys
        for model in self.semantic_layer.models:
            if not model.primaryKey:
                report["warnings"].append(
                    f"Model '{model.name}' has no primary key defined"
                )
        
        return report


# ===== UTILITY FUNCTIONS =====

def create_mdl_template(domain: str, output_path: str) -> str:
    """Create MDL template for a specific domain"""
    templates = {
        "customer_service": {
            "catalog": "customer_service_analytics",
            "schema": "main",
            "dataSource": "LOCAL_FILE",
            "models": [
                {
                    "name": "tickets",
                    "tableReference": "data/customer_service.csv",
                    "columns": [
                        {"name": "ticket_id", "type": "STRING"},
                        {"name": "created_date", "type": "DATE"},
                        {"name": "status", "type": "STRING"},
                        {"name": "priority", "type": "STRING"},
                    ],
                    "primaryKey": "ticket_id"
                }
            ],
            "relationships": [],
            "metrics": []
        }
    }
    
    template = templates.get(domain)
    if not template:
        raise ValueError(f"Unknown domain: {domain}")
    
    with open(output_path, 'w') as f:
        yaml.dump(template, f, default_flow_style=False)
    
    return output_path


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        mdl_file = sys.argv[1]
        parser = SemanticLayerParser(mdl_file)
        mdl = parser.load()
        
        # Print validation report
        report = parser.validate()
        print("\n=== VALIDATION REPORT ===")
        print(f"Valid: {report['valid']}")
        print(f"Stats: {report['stats']}")
        if report['errors']:
            print(f"Errors: {report['errors']}")
        if report['warnings']:
            print(f"Warnings: {report['warnings']}")
        
        # Test context generation
        test_query = "What is the average resolution time?"
        context = parser.generate_context(test_query)
        print(f"\n=== CONTEXT FOR: '{test_query}' ===")
        print(context)
    else:
        print("Usage: python semantic_layer.py <mdl_file.yaml>")
