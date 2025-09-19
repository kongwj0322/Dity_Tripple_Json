// Cypher normalization script for Untitled-5.json
// This script applies all 8 normalization rules systematically

// 1) 表现为/具有 → 上位类(地质条件/水文条件) 统一为 属于
MATCH (a)-[r]->(b)
WHERE r.relation_type='属性关系'
  AND r.predicate IN ['表现为','具有']
  AND b.name IN ['地质条件','水文条件']
SET r.predicate='属于', r.weight = coalesce(r.weight, 0.5);

// Remove duplicates after transformation
MATCH (a)-[r1]->(b), (a)-[r2]->(b)
WHERE r1.relation_type='属性关系' AND r2.relation_type='属性关系'
  AND r1.predicate='属于' AND r2.predicate='属于'
  AND id(r1) < id(r2)
DELETE r2;

// 2) 监测类"X 波动/异常/升高/不足"统一标注为 Monitoring
MATCH (a)-[r]->(b)
WHERE r.relation_type='因果关系' AND a.name =~ '.*(波动|异常|升高|不足).*'
SET a.subject_type = 'Monitoring';

// 3) 设备综合故障统一为中间态
MATCH (s {name:'施工设备'})-[r {predicate:'导致'}]->(m {name:'设备综合故障'})
SET m.object_type='IntermediateState';
MATCH (m {name:'设备综合故障'}) SET m.subject_type='IntermediateState';

// Ensure all outgoing edges from 设备综合故障 have correct subject_type
MATCH (m {name:'设备综合故障'})-[r]->(target)
WHERE r.relation_type='因果关系'
SET m.subject_type='IntermediateState';

// 4) 修正具体故障事件类型
MATCH (n {name:'主轴承损伤'})-[r]->(target)
SET n.subject_type='Event';
MATCH (source)-[r]->(n {name:'主轴承损伤'})
SET n.object_type='Event';

MATCH (n {name:'密封系统失效'})-[r]->(target)
SET n.subject_type='Event';
MATCH (source)-[r]->(n {name:'密封系统失效'})
SET n.object_type='Event';

MATCH (n {name:'螺旋机扭矩升高'})-[r]->(target)
SET n.subject_type='Monitoring';
MATCH (source)-[r]->(n {name:'螺旋机扭矩升高'})
SET n.object_type='Monitoring';

MATCH (n {name:'土压波动增大'})-[r]->(target)
SET n.subject_type='Monitoring';
MATCH (source)-[r]->(n {name:'土压波动增大'})
SET n.object_type='Monitoring';

// 5) 土压波动增大 归到 监测系统（若此前错误归类到"土压"）
MATCH (a {name:'土压波动增大'})-[r:属性关系]->(b {name:'土压'})
SET r.object='监测系统', r.object_type='RiskFactor', r.weight=0.5;

// 6) 替换：塌方类型 ↔ TBM隧道塌方 的归属关系
MATCH (a {name:'塌方类型'})-[r {predicate:'属于', relation_type:'属性关系'}]->(b {name:'TBM隧道塌方'})
DELETE r;
MERGE (b)-[:属性关系 {predicate:'具有类型', weight:0.4, prior_probability:0}]->(a);

// 7) 删除非规范谓词边并添加替换边
MATCH (a {name:'风险预警触发'})-[r {predicate:'被忽视或响应滞后'}]->(b {name:'应急处置不当或滞后'})
DELETE r;

// Add replacement edge
MERGE (trigger:Node {name:'风险预警触发'})
MERGE (response:Node {name:'预警响应启动'})
MERGE (trigger)-[:因果关系 {predicate:'导致', weight:0.6, prior_probability:0, subject_type:'Monitoring', object_type:'Human'}]->(response);

// Handle 监测频率不足 -> 监测盲区形成 replacement
MATCH (a {name:'监测频率'})-[r {predicate:'不足导致'}]->(b {name:'监测盲区形成'})
DELETE r;
MERGE (insufficient:Node {name:'监测频率不足', subject_type:'Monitoring'})
MERGE (insufficient)-[:因果关系 {predicate:'导致', weight:0.8, prior_probability:0, object_type:'RiskFactor'}]->(b);

// 8) 解决"沉降速率阈值"的双重归属
MATCH (a {name:'沉降速率阈值'})-[r {predicate:'属于', relation_type:'属性关系'}]->(b {name:'监测指标'})
DELETE r;
MERGE (ctrl:Node {name:'控制指标', subject_type:'RiskFactor'})
MERGE (moni:Node {name:'监测指标', object_type:'RiskFactor'})
MERGE (a)-[:属性关系 {predicate:'属于', weight:0.5, prior_probability:0, object_type:'RiskFactor'}]->(ctrl)
MERGE (ctrl)-[:属性关系 {predicate:'属于', weight:0.4, prior_probability:0, object_type:'RiskFactor'}]->(moni);

// 9) 下调 属性/位置 关系权重至中位
MATCH ()-[r]->()
WHERE r.relation_type IN ['属性关系','位置关系'] AND r.weight > 0.6
SET r.weight = 0.5;

// 10) 统一替换所有 "不足导致" 为 "导致"
MATCH ()-[r]->()
WHERE r.predicate = '不足导致'
SET r.predicate = '导致';