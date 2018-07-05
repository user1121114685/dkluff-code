---------禁用100级以上技能

select * into [ECSRO_SHARD].[dbo].[_RefSkill_backup]
from [ECSRO_SHARD].[dbo].[_RefSkill]

update [ECSRO_SHARD].[dbo].[_RefSkill]
set Service = 0
where ReqCommon_MasteryLevel1 >=100

SELECT *
  FROM [ECSRO_SHARD].[dbo].[_RefSkill]
  where ReqCommon_MasteryLevel1 >=100


----rename table
EXEC sp_rename 'ECSRO_ACCOUNT', 'VSRO_ACCOUNT','DATABASE';
EXEC sp_rename 'ECSRO_LOG', 'VSRO_LOG','DATABASE';
EXEC sp_rename 'ECSRO_SHARD', 'VSRO_SHARD','DATABASE';