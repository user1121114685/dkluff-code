exec [BR_ACCOUNT].[dbo].[_AddUser] 'cc','202cb962ac59075b964b07152d234b70',null,null,null,null,null,3,3,null

declare @uid int;
set @uid = @uid;

/*insert into [dbo].[_CharSkillMastery]
values (@uid,257,100);*/

/*更新技能等级*/
update [dbo].[_CharSkillMastery]
set [Level] = 100 
where [CharID] = @uid;

/*角色属性*/
update [dbo].[_Char]
set [CurLevel] = 100,[MaxLevel]=100,
    [RemainGold]=10000000000,
    [Strength] = 1000,[Intellect]=1000,
	[RemainSkillPoint]=2000000
where [CharID] = @uid;

/*技能全修 会崩溃*/
use [BR_SHARD]
declare @uid int
set @uid = 3009

DELETE FROM [dbo].[_CharSkill] where [CharID] =@uid

INSERT INTO [dbo].[_CharSkill] ( CharID,SkillID,[Enable] )
SELECT [CharID] =@uid,max(ID) as SkillID , [Enable]=1
FROM [BR_SHARD].[dbo].[_RefSkill]
where Service =1 AND [Basic_Group] like 'SKILL_CH_%' AND ID>2000 and ReqLearn_SP>0 GROUP BY [Basic_Group]

INSERT INTO [dbo].[_CharSkill] ( CharID,SkillID,[Enable] )
SELECT [CharID] =@uid,max(ID) as SkillID , [Enable]=1
FROM [BR_SHARD].[dbo].[_RefSkill]
where Service =1 AND [Basic_Group] like 'SKILL_CH_%' AND ID<2000 GROUP BY [Basic_Group]
---------------------
use [BR_SHARD]
declare @uid int
set @uid = 3010

DELETE FROM [dbo].[_CharSkill] where [CharID] =@uid

INSERT INTO [dbo].[_CharSkill] ( CharID,SkillID,[Enable] )
SELECT [CharID] =@uid, SkillID , [Enable]=1
FROM [dbo].[FullSkill]


-------------------
/*商城*/
DELETE FROM [ECSRO_ACCOUNT].[dbo].[SK_Silk]
where JID = @juid
INSERT INTO [ECSRO_ACCOUNT].[dbo].[SK_Silk]
VALUES (@juid,9999,9999,9999)

/*物品*/
EXEC  [dbo].[_ADD_ITEM_EXTERN] 'qqqq','ITEM_CH_TBLADE_13_C_RARE', 255,12
/*
ITEM_CH_BLADE_13_C_RARE
ITEM_CH_BOW_13_C_RARE
ITEM_CH_EARRING_13_C_RARE
ITEM_CH_M_CLOTHES_13_AA_C_RARE
ITEM_CH_M_CLOTHES_13_BA_C_RARE
ITEM_CH_M_CLOTHES_13_CA_C_RARE
ITEM_CH_M_CLOTHES_13_FA_C_RARE
ITEM_CH_M_CLOTHES_13_HA_C_RARE
ITEM_CH_M_CLOTHES_13_LA_C_RARE
ITEM_CH_M_CLOTHES_13_SA_C_RARE
ITEM_CH_M_HEAVY_13_AA_C_RARE
ITEM_CH_M_HEAVY_13_BA_C_RARE
ITEM_CH_M_HEAVY_13_CA_C_RARE
ITEM_CH_M_HEAVY_13_FA_C_RARE
ITEM_CH_M_HEAVY_13_HA_C_RARE
ITEM_CH_M_HEAVY_13_LA_C_RARE
ITEM_CH_M_HEAVY_13_SA_C_RARE
ITEM_CH_M_LIGHT_13_AA_C_RARE
ITEM_CH_M_LIGHT_13_BA_C_RARE
ITEM_CH_M_LIGHT_13_CA_C_RARE
ITEM_CH_M_LIGHT_13_FA_C_RARE
ITEM_CH_M_LIGHT_13_HA_C_RARE
ITEM_CH_M_LIGHT_13_LA_C_RARE
ITEM_CH_M_LIGHT_13_SA_C_RARE
ITEM_CH_NECKLACE_13_C_RARE
ITEM_CH_RING_13_C_RARE
ITEM_CH_SHIELD_13_C_RARE
ITEM_CH_SPEAR_13_C_RARE
ITEM_CH_SWORD_13_C_RARE
ITEM_CH_TBLADE_13_C_RARE
ITEM_CH_W_CLOTHES_13_AA_C_RARE
ITEM_CH_W_CLOTHES_13_BA_C_RARE
ITEM_CH_W_CLOTHES_13_CA_C_RARE
ITEM_CH_W_CLOTHES_13_FA_C_RARE
ITEM_CH_W_CLOTHES_13_HA_C_RARE
ITEM_CH_W_CLOTHES_13_LA_C_RARE
ITEM_CH_W_CLOTHES_13_SA_C_RARE
ITEM_CH_W_HEAVY_13_AA_C_RARE
ITEM_CH_W_HEAVY_13_BA_C_RARE
ITEM_CH_W_HEAVY_13_CA_C_RARE
ITEM_CH_W_HEAVY_13_FA_C_RARE
ITEM_CH_W_HEAVY_13_HA_C_RARE
ITEM_CH_W_HEAVY_13_LA_C_RARE
ITEM_CH_W_HEAVY_13_SA_C_RARE
ITEM_CH_W_LIGHT_13_AA_C_RARE
ITEM_CH_W_LIGHT_13_BA_C_RARE
ITEM_CH_W_LIGHT_13_CA_C_RARE
ITEM_CH_W_LIGHT_13_FA_C_RARE
ITEM_CH_W_LIGHT_13_HA_C_RARE
ITEM_CH_W_LIGHT_13_LA_C_RARE
ITEM_CH_W_LIGHT_13_SA_C_RARE
*/
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_BLADE_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_BOW_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_EARRING_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_13_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_13_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_13_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_13_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_13_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_13_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_13_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_13_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_13_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_13_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_13_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_13_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_13_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_13_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_13_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_13_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_13_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_13_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_13_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_13_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_13_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_NECKLACE_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_RING_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_RING_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_SHIELD_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_SPEAR_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_SWORD_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_TBLADE_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_13_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_13_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_13_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_13_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_13_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_13_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_13_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_13_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_13_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_13_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_13_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_13_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_13_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_13_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_13_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_13_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_13_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_13_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_13_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_13_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_13_SA_C_RARE',255,12

--------------------EU---------------
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_DAGGER_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_SWORD_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_TSWORD_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_AXE_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_CROSSBOW_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_DARKSTAFF_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_TSTAFF_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_HARP_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_STAFF_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_SHIELD_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_HEAVY_13_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_HEAVY_13_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_HEAVY_13_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_HEAVY_13_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_HEAVY_13_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_HEAVY_13_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_HEAVY_13_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_LIGHT_13_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_LIGHT_13_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_LIGHT_13_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_LIGHT_13_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_LIGHT_13_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_LIGHT_13_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_LIGHT_13_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_CLOTHES_13_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_CLOTHES_13_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_CLOTHES_13_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_CLOTHES_13_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_CLOTHES_13_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_CLOTHES_13_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_M_CLOTHES_13_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_HEAVY_13_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_HEAVY_13_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_HEAVY_13_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_HEAVY_13_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_HEAVY_13_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_HEAVY_13_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_HEAVY_13_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_LIGHT_13_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_LIGHT_13_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_LIGHT_13_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_LIGHT_13_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_LIGHT_13_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_LIGHT_13_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_LIGHT_13_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_CLOTHES_13_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_CLOTHES_13_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_CLOTHES_13_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_CLOTHES_13_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_CLOTHES_13_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_CLOTHES_13_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_W_CLOTHES_13_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_RING_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_RING_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_EARRING_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_EU_NECKLACE_13_C_RARE',255,12

--------------EU SKILL----------------------
use [BR_SHARD]
declare @uid int
set @uid = 3021

DELETE FROM [dbo].[_CharSkill] where [CharID] =@uid

INSERT INTO [dbo].[_CharSkill] ( CharID,SkillID,[Enable] )
SELECT [CharID] =@uid,max(ID) as SkillID , [Enable]=1
FROM [BR_SHARD].[dbo].[_RefSkill]
where Service =1 AND [Basic_Group] like 'SKILL_EU_%' AND ID<8000  GROUP BY [Basic_Group]

INSERT INTO [dbo].[_CharSkill] ( CharID,SkillID,[Enable] )
SELECT [CharID] =@uid,max(ID) as SkillID , [Enable]=1
FROM [BR_SHARD].[dbo].[_RefSkill]
where Service =1 AND [Basic_Group] like 'SKILL_EU_%' AND ID>=9000 and ID<10000 GROUP BY [Basic_Group]