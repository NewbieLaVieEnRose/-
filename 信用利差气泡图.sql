SELECT
	AA.*,
	BB.`成交量(手)`,
	CC.`债券期限(年)`,
	CC.`发行人`,
	DD.`所属区县` 
FROM
	( SELECT * FROM `信用利差_国开债` ) AA
	LEFT JOIN ( SELECT `Wind代码`, `交易日期`, `成交量(手)` FROM `天津城投债日行情` ) BB ON AA.`Wind代码` = BB.`Wind代码` 
	AND AA.`交易日期` = BB.`交易日期`
	LEFT JOIN ( SELECT `Wind代码`, `发行人`, `债券期限(年)` FROM `天津城投债基本资料` ) CC ON AA.`Wind代码` = CC.`Wind代码`
	LEFT JOIN ( SELECT `发行人`, `所属区县` FROM `天津城投主体详情` ) DD ON CC.`发行人` = DD.`发行人`