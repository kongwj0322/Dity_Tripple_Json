#!/usr/bin/env python3
"""
TBM Collapse Mechanism Builder

This script transforms raw triples data into hierarchical mechanism chains
for TBM collapse risk analysis, replacing direct causal edges to "TBM隧道塌方"
with detailed multi-hop mechanism pathways.
"""

import json
import os
from typing import List, Dict, Any

class TBMMechanismBuilder:
    def __init__(self):
        self.mechanism_chains = self._define_mechanism_chains()
        
    def _define_mechanism_chains(self) -> Dict[str, List[Dict]]:
        """Define mechanism chain patterns based on transformation rules"""
        return {
            # A) Equipment/Tools failures
            "主轴承损伤": [
                {"subject": "主轴承损伤", "object": "刀盘转速异常", "object_type": "Methods&Params", "predicate": "导致"},
                {"subject": "刀盘转速异常", "object": "扭矩异常", "object_type": "Methods&Params", "predicate": "导致"},
                {"subject": "扭矩异常", "object": "仓压差异常", "object_type": "Methods&Params", "predicate": "导致"},
                {"subject": "仓压差异常", "object": "土压不足", "object_type": "Methods&Params", "predicate": "导致"},
                {"subject": "土压不足", "object": "掌子面失稳", "object_type": "Event", "predicate": "导致"},
                {"subject": "掌子面失稳", "object": "掌子面坍塌", "object_type": "CollapseType", "predicate": "触发"},
                {"subject": "掌子面坍塌", "object": "TBM隧道塌方", "object_type": "RiskResult", "predicate": "触发"}
            ],
            
            # B) Methods & Params - injection related
            "二次注浆量过大": [
                {"subject": "二次注浆量过大", "object": "浆液侵入扰动", "object_type": "Event", "predicate": "导致"},
                {"subject": "浆液侵入扰动", "object": "地层扰动增大", "object_type": "Event", "predicate": "导致"},
                {"subject": "地层扰动增大", "object": "围岩承载力降低", "object_type": "Event", "predicate": "导致"},
                {"subject": "围岩承载力降低", "object": "侧壁围岩失稳滑移", "object_type": "Event", "predicate": "导致"},
                {"subject": "侧壁围岩失稳滑移", "object": "洞身段塌方", "object_type": "CollapseType", "predicate": "触发"},
                {"subject": "洞身段塌方", "object": "TBM隧道塌方", "object_type": "RiskResult", "predicate": "触发"}
            ],
            
            "注浆时间过长": [
                {"subject": "注浆时间过长", "object": "浆液侵入扰动", "object_type": "Event", "predicate": "导致"},
                {"subject": "浆液侵入扰动", "object": "地层扰动增大", "object_type": "Event", "predicate": "导致"},
                {"subject": "地层扰动增大", "object": "围岩承载力降低", "object_type": "Event", "predicate": "导致"},
                {"subject": "围岩承载力降低", "object": "侧壁围岩失稳滑移", "object_type": "Event", "predicate": "导致"},
                {"subject": "侧壁围岩失稳滑移", "object": "洞身段塌方", "object_type": "CollapseType", "predicate": "触发"},
                {"subject": "洞身段塌方", "object": "TBM隧道塌方", "object_type": "RiskResult", "predicate": "触发"}
            ],
            
            "同步注浆量不足": [
                {"subject": "同步注浆量不足", "object": "盾尾空隙过大", "object_type": "Event", "predicate": "导致"},
                {"subject": "盾尾空隙过大", "object": "地表沉降超限", "object_type": "Event", "predicate": "导致"},
                {"subject": "地表沉降超限", "object": "初期支护背后空洞", "object_type": "Event", "predicate": "导致"},
                {"subject": "初期支护背后空洞", "object": "洞身段塌方", "object_type": "CollapseType", "predicate": "触发"},
                {"subject": "洞身段塌方", "object": "TBM隧道塌方", "object_type": "RiskResult", "predicate": "触发"}
            ],
            
            # B) Methods & Params - mud/slurry parameters
            "泥浆比重过低": [
                {"subject": "泥浆比重过低", "object": "土体改良效果差", "object_type": "Event", "predicate": "导致"},
                {"subject": "土体改良效果差", "object": "渣土流变性劣化", "object_type": "Event", "predicate": "导致"},
                {"subject": "渣土流变性劣化", "object": "面压控制困难", "object_type": "Event", "predicate": "导致"},
                {"subject": "面压控制困难", "object": "仓压差异常", "object_type": "Methods&Params", "predicate": "导致"},
                {"subject": "仓压差异常", "object": "土压不足", "object_type": "Methods&Params", "predicate": "导致"},
                {"subject": "土压不足", "object": "掌子面失稳", "object_type": "Event", "predicate": "导致"},
                {"subject": "掌子面失稳", "object": "掌子面坍塌", "object_type": "CollapseType", "predicate": "触发"},
                {"subject": "掌子面坍塌", "object": "TBM隧道塌方", "object_type": "RiskResult", "predicate": "触发"}
            ],
            
            "泥水压力不足": [
                {"subject": "泥水压力不足", "object": "掌子面失稳", "object_type": "Event", "predicate": "导致"},
                {"subject": "掌子面失稳", "object": "掌子面坍塌", "object_type": "CollapseType", "predicate": "触发"},
                {"subject": "掌子面坍塌", "object": "TBM隧道塌方", "object_type": "RiskResult", "predicate": "触发"}
            ],
            
            # B) Methods & Params - advancing speed
            "推进速度过大": [
                {"subject": "推进速度过大", "object": "贯入度过大", "object_type": "Methods&Params", "predicate": "导致"},
                {"subject": "贯入度过大", "object": "扭矩不足", "object_type": "Methods&Params", "predicate": "导致"},
                {"subject": "扭矩不足", "object": "仓压差异常", "object_type": "Methods&Params", "predicate": "导致"},
                {"subject": "仓压差异常", "object": "土压异常", "object_type": "Methods&Params", "predicate": "导致"},
                {"subject": "土压异常", "object": "掌子面失稳", "object_type": "Event", "predicate": "导致"},
                {"subject": "掌子面失稳", "object": "掌子面坍塌", "object_type": "CollapseType", "predicate": "触发"},
                {"subject": "掌子面坍塌", "object": "TBM隧道塌方", "object_type": "RiskResult", "predicate": "触发"}
            ],
            
            "推进速度过小": [
                {"subject": "推进速度过小", "object": "贯入度过小", "object_type": "Methods&Params", "predicate": "导致"},
                {"subject": "贯入度过小", "object": "扭矩过大", "object_type": "Methods&Params", "predicate": "导致"},
                {"subject": "扭矩过大", "object": "仓压差异常", "object_type": "Methods&Params", "predicate": "导致"},
                {"subject": "仓压差异常", "object": "土压异常", "object_type": "Methods&Params", "predicate": "导致"},
                {"subject": "土压异常", "object": "掌子面失稳", "object_type": "Event", "predicate": "导致"},
                {"subject": "掌子面失稳", "object": "掌子面坍塌", "object_type": "CollapseType", "predicate": "触发"},
                {"subject": "掌子面坍塌", "object": "TBM隧道塌方", "object_type": "RiskResult", "predicate": "触发"}
            ],
            
            # General mechanism for parameters that affect stability
            "沉降速率阈值": [
                {"subject": "沉降速率阈值", "object": "围岩自稳能力差", "object_type": "Event", "predicate": "导致"},
                {"subject": "围岩自稳能力差", "object": "掌子面稳定性降低", "object_type": "Event", "predicate": "导致"},
                {"subject": "掌子面稳定性降低", "object": "掌子面失稳", "object_type": "Event", "predicate": "导致"},
                {"subject": "掌子面失稳", "object": "掌子面坍塌", "object_type": "CollapseType", "predicate": "触发"},
                {"subject": "掌子面坍塌", "object": "TBM隧道塌方", "object_type": "RiskResult", "predicate": "触发"}
            ],
            
            # Already processed events
            "侧壁围岩失稳滑移": [
                {"subject": "侧壁围岩失稳滑移", "object": "洞身段塌方", "object_type": "CollapseType", "predicate": "触发"},
                {"subject": "洞身段塌方", "object": "TBM隧道塌方", "object_type": "RiskResult", "predicate": "触发"}
            ]
        }
    
    def calculate_weights(self, original_weight: str, chain_length: int) -> List[str]:
        """Calculate weights for mechanism chain with decreasing pattern"""
        try:
            base_weight = float(original_weight)
        except (ValueError, TypeError):
            print(f"Warning: Could not parse weight '{original_weight}', using default 0.8000")
            base_weight = 0.8000
        
        weights = []
        for i in range(chain_length):
            if i == 0:
                # First hop keeps original weight
                weight = base_weight
            else:
                # Subsequent hops decrease by 0.0001 per hop
                weight = base_weight - (i * 0.0001)
            
            # Keep within bounds and format to 4 decimals
            weight = max(0.7500, min(0.8500, weight))  # Allow higher upper bound
            weights.append(f"{weight:.4f}")
        
        return weights
    
    def create_mechanism_chain(self, original_triple: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create mechanism chain for a given triple"""
        subject = original_triple["subject"]
        
        # Find matching chain pattern
        chain_template = self.mechanism_chains.get(subject)
        if not chain_template:
            # Default fallback for unmatched subjects
            chain_template = [
                {"subject": subject, "object": "掌子面失稳", "object_type": "Event", "predicate": "导致"},
                {"subject": "掌子面失稳", "object": "掌子面坍塌", "object_type": "CollapseType", "predicate": "触发"},
                {"subject": "掌子面坍塌", "object": "TBM隧道塌方", "object_type": "RiskResult", "predicate": "触发"}
            ]
        
        # Calculate weights for the chain
        weights = self.calculate_weights(original_triple.get("weight", "0.8000"), len(chain_template))
        
        # Create chain edges
        chain_edges = []
        for i, template_edge in enumerate(chain_template):
            edge = {
                "subject": template_edge["subject"],
                "parent_subject_type": original_triple.get("parent_subject_type", "RiskFactor"),
                "subject_type": original_triple["subject_type"] if i == 0 else template_edge.get("subject_type", "Event"),
                "weight": weights[i],
                "prior_probability": original_triple.get("prior_probability", "0"),
                "predicate": template_edge["predicate"],
                "object": template_edge["object"],
                "object_type": template_edge["object_type"],
                "relation_type": "因果关系"
            }
            chain_edges.append(edge)
        
        return chain_edges
    
    def process_triples(self, input_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process all triples and transform causal edges to TBM隧道塌方"""
        output_edges = []
        edge_set = set()  # For deduplication
        
        for triple in input_data:
            # Check if this is a causal edge to TBM隧道塌方
            if (triple.get("relation_type") == "因果关系" and 
                triple.get("object") == "TBM隧道塌方"):
                
                # Replace with mechanism chain
                chain_edges = self.create_mechanism_chain(triple)
                
                for edge in chain_edges:
                    # Create edge key for deduplication
                    edge_key = (edge["subject"], edge["predicate"], edge["object"], edge["relation_type"])
                    
                    if edge_key not in edge_set:
                        edge_set.add(edge_key)
                        output_edges.append(edge)
                    else:
                        # Keep edge with higher weight if duplicate
                        for i, existing_edge in enumerate(output_edges):
                            existing_key = (existing_edge["subject"], existing_edge["predicate"], 
                                          existing_edge["object"], existing_edge["relation_type"])
                            if existing_key == edge_key:
                                if float(edge["weight"]) > float(existing_edge["weight"]):
                                    output_edges[i] = edge
                                break
            else:
                # Copy non-causal edges directly
                output_edges.append(triple)
        
        return output_edges

def main():
    """Main function to build mechanism JSON"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    
    input_file = os.path.join(repo_root, "data", "raw_input.json")
    output_file = os.path.join(repo_root, "data", "TBM_collapse_mechanism_full.json")
    
    # Load input data
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
        print(f"Loaded {len(input_data)} triples from {input_file}")
    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {input_file}: {e}")
        return
    
    # Build mechanism chains
    builder = TBMMechanismBuilder()
    output_data = builder.process_triples(input_data)
    
    # Write output
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"Generated {len(output_data)} edges in {output_file}")
        
        # Report statistics
        causal_edges = [e for e in output_data if e.get("relation_type") == "因果关系"]
        direct_tbm_edges = [e for e in causal_edges if e.get("object") == "TBM隧道塌方"]
        print(f"Total causal edges: {len(causal_edges)}")
        print(f"Direct edges to TBM隧道塌方: {len(direct_tbm_edges)}")
        
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    main()