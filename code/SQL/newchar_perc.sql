USE [BR_SHARD]
GO
/****** Object:  StoredProcedure [dbo].[_AddNewChar]    Script Date: 2018/6/23 2:29:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[_AddNewChar]  
@UserJID   INT,  
--@CharSlot   INT,  
@RefCharID   INT,  
@CharName   varchar (64),  
@CharScale   tinyINT,  
@StartRegionID   INT,  
@StartPos_X   real,  
@StartPos_Y   real,  
@StartPos_Z   real,  
@DefaultTeleport  INT,  
@RefMailID   INT,  
@RefPantsID   INT,  
@RefBootsID   INT,  
@RefWeaponID  INT,  
@DurMail   tinyINT,  
@DurPants   tinyINT,  
@DurBoots   tinyINT,  
@DurWeapon   tinyINT,  
@DefaultArrow   INT  
AS  
    -- Initial Equip Edit by LemoniscooL
 DECLARE @RefHandID INT
 DECLARE @RefHatID INT
 DECLARE @RefShoulderID INT
 DECLARE @RefEarringID INT
 DECLARE @RefRingID INT
 DECLARE @RefNeckID INT
 DECLARE @DurHand INT
 DECLARE @DurHat INT
 DECLARE @DurShoulder INT
 DECLARE @DurEarring INT
 DECLARE @DurRing INT
 DECLARE @DurNeck INT
 
 IF (@RefMailID = 3643) BEGIN
	SET @RefHandID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_M_CLOTHES_01_AA_RARE')
	SET @RefMailID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_M_CLOTHES_01_BA_RARE')
	SET @RefBootsID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_M_CLOTHES_01_FA_RARE')
	SET @RefHatID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_M_CLOTHES_01_HA_RARE')
	SET @RefPantsID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_M_CLOTHES_01_LA_RARE')
	SET @RefShoulderID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_M_CLOTHES_01_SA_RARE')
	SET @RefEarringID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_EARRING_01_C_RARE')
	SET @RefNeckID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_NECKLACE_01_C_RARE')
	SET @RefRingID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_RING_01_C_RARE')
 END
 	
	
 --Male Heavy Armor Chinese
 IF (@RefMailID = 3637) BEGIN
	SET @RefHandID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_M_HEAVY_01_AA_RARE')
	SET @RefMailID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_M_HEAVY_01_BA_RARE')
	SET @RefBootsID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_M_HEAVY_01_FA_RARE')
	SET @RefHatID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_M_HEAVY_01_HA_RARE')
	SET @RefPantsID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_M_HEAVY_01_LA_RARE')
	SET @RefShoulderID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_M_HEAVY_01_SA_RARE')
	SET @RefEarringID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_EARRING_01_C_RARE')
	SET @RefNeckID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_NECKLACE_01_C_RARE')
	SET @RefRingID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_RING_01_C_RARE')
 END
 
 --Male Light Armor Chinese
 IF (@RefMailID = 3640) BEGIN
	SET @RefHandID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_M_LIGHT_01_AA_RARE')
	SET @RefMailID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_M_LIGHT_01_BA_RARE')
	SET @RefBootsID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_M_LIGHT_01_FA_RARE')
	SET @RefHatID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_M_LIGHT_01_HA_RARE')
	SET @RefPantsID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_M_LIGHT_01_LA_RARE')
	SET @RefShoulderID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_M_LIGHT_01_SA_RARE')
	SET @RefEarringID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_EARRING_01_C_RARE')
	SET @RefNeckID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_NECKLACE_01_C_RARE')
	SET @RefRingID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_RING_01_C_RARE')
 END
 
 --Female Clothes Chinese
 IF (@RefMailID = 3652) BEGIN
	SET @RefHandID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_W_CLOTHES_01_AA_RARE')
	SET @RefMailID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_W_CLOTHES_01_BA_RARE')
	SET @RefBootsID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_W_CLOTHES_01_FA_RARE')
	SET @RefHatID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_W_CLOTHES_01_HA_RARE')
	SET @RefPantsID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_W_CLOTHES_01_LA_RARE')
	SET @RefShoulderID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_W_CLOTHES_01_SA_RARE')
	SET @RefEarringID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_EARRING_01_C_RARE')
	SET @RefNeckID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_NECKLACE_01_C_RARE')
	SET @RefRingID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_RING_01_C_RARE')
 END
 
 --Female Heavy Armor Chinese
 IF (@RefMailID = 3646) BEGIN
	SET @RefHandID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_W_HEAVY_01_AA_RARE')
	SET @RefMailID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_W_HEAVY_01_BA_RARE')
	SET @RefBootsID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_W_HEAVY_01_FA_RARE')
	SET @RefHatID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_W_HEAVY_01_HA_RARE')
	SET @RefPantsID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_W_HEAVY_01_LA_RARE')
	SET @RefShoulderID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_W_HEAVY_01_SA_RARE')
	SET @RefEarringID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_EARRING_01_C_RARE')
	SET @RefNeckID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_NECKLACE_01_C_RARE')
	SET @RefRingID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_RING_01_C_RARE')
 END
 
 --Female Light Armor Chinese
 IF (@RefMailID = 3649) BEGIN
	SET @RefHandID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_W_LIGHT_01_AA_RARE')
	SET @RefMailID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_W_LIGHT_01_BA_RARE')
	SET @RefBootsID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_W_LIGHT_01_FA_RARE')
	SET @RefHatID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_W_LIGHT_01_HA_RARE')
	SET @RefPantsID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_W_LIGHT_01_LA_RARE')
	SET @RefShoulderID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_W_LIGHT_01_SA_RARE')
	SET @RefEarringID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_EARRING_01_C_RARE')
	SET @RefNeckID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_NECKLACE_01_C_RARE')
	SET @RefRingID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_RING_01_C_RARE')
 END

 --Blade Chinese
 IF (@RefWeaponID = 3633) BEGIN
	SET @RefWeaponID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_BLADE_01_C_RARE')
 END
 
 --Bow Chinese
 IF (@RefWeaponID = 3636) BEGIN
	SET @RefWeaponID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_BOW_01_C_RARE')
 END
 
 --Spear Chinese
 IF (@RefWeaponID = 3634) BEGIN
	SET @RefWeaponID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_SPEAR_01_C_RARE')
 END
 
 --Sword Chinese
 IF (@RefWeaponID = 3632) BEGIN
	SET @RefWeaponID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_SWORD_01_C_RARE')
 END
 
 --Glavie Chinese
 IF (@RefWeaponID = 3635) BEGIN
	SET @RefWeaponID = (SELECT ID FROM _RefObjCommon WHERE CodeName128='ITEM_CH_TBLADE_01_C_RARE')
 END
 
 --Select Durability
 SET @DurHand = (Select Dur_L from _RefObjItem where ID in (Select Link from _RefObjCommon where ID = @RefHandID))
 SET @DurMail = (Select Dur_L from _RefObjItem where ID in (Select Link from _RefObjCommon where ID = @RefMailID))
 SET @DurBoots = (Select Dur_L from _RefObjItem where ID in (Select Link from _RefObjCommon where ID = @RefBootsID))
 SET @DurHat = (Select Dur_L from _RefObjItem where ID in (Select Link from _RefObjCommon where ID = @RefHatID))
 SET @DurPants = (Select Dur_L from _RefObjItem where ID in (Select Link from _RefObjCommon where ID = @RefPantsID))
 SET @DurShoulder = (Select Dur_L from _RefObjItem where ID in (Select Link from _RefObjCommon where ID = @RefShoulderID))
 SET @DurWeapon = (Select Dur_L from _RefObjItem where ID in (Select Link from _RefObjCommon where ID = @RefWeaponID))
 SET @DurEarring = (Select Dur_L from _RefObjItem where ID in (Select Link from _RefObjCommon where ID = @RefEarringID))
 SET @DurRing = (Select Dur_L from _RefObjItem where ID in (Select Link from _RefObjCommon where ID = @RefRingID))
 SET @DurNeck = (Select Dur_L from _RefObjItem where ID in (Select Link from _RefObjCommon where ID = @RefNeckID))



DECLARE @Slot  INT  
 DECLARE @temp  INT  
    
		
 DECLARE @NewCharID  INT  
 SET @NewCharID = 0  
  
 set xact_abort on  
   
BEGIN TRANSACTION  
   
 -----------------------------------------------------------------------------  
 -- 1. 캐릭터 슬롯 넘버가 valid한 것인지, 그리고 빈슬롯이 맞는지 먼저 체크한다.  
 -----------------------------------------------------------------------------  
  
 /* -- commented by novice. for server integration.  
 IF (@CharSlot = 0)  
  BEGIN SELECT @temp = CharID1 FROM _User  WITH (NOLOCK) WHERE UserJID = @UserJID END  
 ELSE IF (@CharSlot = 1)  
  BEGIN SELECT @temp = CharID2 FROM _User  WITH (NOLOCK) WHERE UserJID = @UserJID END  
 ELSE IF (@CharSlot = 2)  
  BEGIN SELECT @temp = CharID3 FROM _User  WITH (NOLOCK) WHERE UserJID = @UserJID END  
 ELSE   
  BEGIN -- 가능한 캐릭터 슬롯은 1,2,3 이렇게 3개 뿐이라고!  
   ROLLBACK TRANSACTION  
   RETURN -1  
  END  
  
 IF (@temp <> 0)  
 BEGIN  
  -- 빈 슬롯이 아니므로 무효!  
  ROLLBACK TRANSACTION  
  RETURN -2  
 END  
 */  
  
 -- start by novice.  
 SELECT @temp = count(CharID) FROM _User WITH (NOLOCK) WHERE UserJID = @UserJID  
  
 IF (@temp >= 3)  
 BEGIN  
  -- 너무 많자나  
  ROLLBACK TRANSACTION  
  RETURN -2  
 END  
 -- finish by novice.  
  
 -----------------------------------------------------------------------------  
 -- 2. 캐릭터 추가하기  
 -----------------------------------------------------------------------------  
 IF (@CharScale > 68) -- 0100 0100 --> 68 이다!  
 BEGIN  
  -- 캐릭터 생성 실패! 스케일 값이 이상하다!   
  ROLLBACK TRANSACTION  
  RETURN -3  
 END  
 EXEC @temp = _IsExistingCharName @CharName  
 IF (@temp <> 0)  
 BEGIN  
  -- 이미 사용중인 이름이라는데?  
  ROLLBACK TRANSACTION  
  RETURN -4  
 END  
 --PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!  
 INSERT INTO _Char ( RefObjID, CharName16, Scale, Strength, Intellect, LatestRegion,PosX, PosY, PosZ, AppointedTeleport, InventorySize,  
    LastLogout, CurLevel, MaxLevel, RemainGold, RemainStatPoint, RemainSkillPoint, HP, MP, JobLvl_Trader, JobLvl_Hunter, JobLvl_Robber)  
     VALUES (@RefCharID, @CharName, @CharScale, 20, 20, @StartRegionID, @StartPos_X, @StartPos_Y, @StartPos_Z, @DefaultTeleport, 77,  
    GetDate(), 1, 1, 0, 0, 0, 200,200, 1, 1, 1)  
 --PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!  
  
 SET @NewCharID = @@IDENTITY  
 IF (@@ERROR <> 0 OR @@ROWCOUNT = 0)  
 BEGIN  
  -- 캐릭터 생성 실패!  
  ROLLBACK TRANSACTION  
  RETURN -5  
 END  
  
 /* -- commented by novice. for server integration.  
 IF (@CharSlot = 0)    
 BEGIN  
  UPDATE _User  SET CharID1 = @NewCharID WHERE UserJID= @UserJID  
 END  
 ELSE IF (@CharSlot = 1)  
 BEGIN  
  UPDATE _User SET CharID2 = @NewCharID WHERE UserJID= @UserJID  
 END  
 ELSE IF (@CharSlot = 2)  
 BEGIN  
  UPDATE _User SET CharID3 = @NewCharID WHERE UserJID = @UserJID  
 END  
 IF (@@ERROR <> 0)  
 BEGIN  
  -- 'User테이블의 캐릭터 슬롯 세팅 실패!  
  ROLLBACK TRANSACTION  
  RETURN -6  
 END  
 */  
   
 -- start by novice.  
 -- 이제 Slot 안쓴다.. 그냥 Insert 만..  
 INSERT INTO _User VALUES (@UserJID, @NewCharID)  
 -- finish by novice.  
  
  
 -----------------------------------------------------------------------------  
 -- 3. 장비 슬롯 채우기  
 -- [인벤토리 슬롯 48개] + [장비슬롯 13개]  
 -----------------------------------------------------------------------------  
        --PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!  
 BEGIN  
  INSERT INTO _Inventory(CharID, Slot, ItemID)  
   SELECT @NewCharID, cnt, 0  
   FROM _RefDummySlot with( nolock )  
   WHERE cnt < 61  
  
  IF (@@ERROR <> 0)  
  BEGIN  
   -- 인벤토리 생성 실패!  
   ROLLBACK TRANSACTION  
   RETURN -7  
  END  
 END  
 --PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!  
   
 -- 디폴트로 선택한 아이템을 다시 넣어주자...  
 /* 요런 순서로  정의되어 있다.  
  0: EQUIP_SLOT_HELM  
  1: EQUIP_SLOT_MAIL,  
  2: EQUIP_SLOT_SHOULDERGUARD,  
  3: EQUIP_SLOT_GAUNTLET,  
  4: EQUIP_SLOT_PANTS,  
  5: EQUIP_SLOT_BOOTS,  
  6: EQUIP_SLOT_WEAPON,  
  7: EQUIP_SLOT_SHIELD or ARROW,  
  8: EQUIP_SLOT_EARRING,  
  9: EQUIP_SLOT_NECKLACE,  
 10: EQUIP_SLOT_L_RING,  
 11: EQUIP_SLOT_R_RING,  
 */  
   
 	 DECLARE @ItemID BIGINT    
 SET @ItemID = 0    
 -- Chest
 IF (@RefMailID <> 0) BEGIN
    EXEC @ItemID =  _FN_ADD_INITIAL_EQUIP @NewCharID, 1, @RefMailID, @DurMail
    IF (@ItemID <= 0) BEGIN
        ROLLBACK TRANSACTION
        RETURN -8
    END
 END
 -- Hand
 IF (@RefHandID <> 0) BEGIN
    EXEC @ItemID =  _FN_ADD_INITIAL_EQUIP @NewCharID, 3, @RefHandID, @DurHand
    IF (@ItemID <= 0) BEGIN
        ROLLBACK TRANSACTION
        RETURN -8
    END
 END
 -- Hat
 IF (@RefHatID <> 0) BEGIN
    EXEC @ItemID =  _FN_ADD_INITIAL_EQUIP @NewCharID, 0, @RefHatID, @DurHat
    IF (@ItemID <= 0) BEGIN
        ROLLBACK TRANSACTION
        RETURN -8
    END
 END
 -- Shoulder
 IF (@RefShoulderID <> 0) BEGIN
    EXEC @ItemID =  _FN_ADD_INITIAL_EQUIP @NewCharID, 2, @RefShoulderID, @DurShoulder
    IF (@ItemID <= 0) BEGIN
        ROLLBACK TRANSACTION
        RETURN -8
    END
 END
 -- Pants 
 IF (@RefPantsID <> 0) BEGIN    
    EXEC @ItemID =  _FN_ADD_INITIAL_EQUIP @NewCharID, 4, @RefPantsID, @DurPants
    IF (@ItemID <= 0) BEGIN    
        ROLLBACK TRANSACTION    
        RETURN -9    
    END    
 END    
 -- Boots    
 IF (@RefBootsID <> 0) BEGIN    
    EXEC @ItemID =  _FN_ADD_INITIAL_EQUIP @NewCharID, 5, @RefBootsID, @DurBoots
    IF (@ItemID <= 0) BEGIN    
        ROLLBACK TRANSACTION    
        RETURN -10    
    END    
 END    
 -- Weapon    
 IF (@RefWeaponID <> 0) BEGIN   
    EXEC @ItemID =  _FN_ADD_INITIAL_EQUIP @NewCharID, 6, @RefWeaponID, @DurWeapon
    IF (@ItemID <= 0) BEGIN    
        ROLLBACK TRANSACTION    
        RETURN -11    
    END    
 END   
 -- Arror/Bolt
 IF (@DefaultArrow <> 0) BEGIN    
    EXEC @ItemID =  _FN_ADD_INITIAL_EQUIP @NewCharID, 7, @DefaultArrow, 250
    IF (@ItemID <= 0) BEGIN    
        ROLLBACK TRANSACTION    
        RETURN -13    
    END    
 END
 -- Earring
 IF (@RefEarringID <> 0) BEGIN
    EXEC @ItemID =  _FN_ADD_INITIAL_EQUIP @NewCharID, 9, @RefEarringID, @DurEarring
    IF (@ItemID <= 0) BEGIN
        ROLLBACK TRANSACTION
        RETURN -8
    END
 END
  -- Necklace
 IF (@RefNeckID <> 0) BEGIN
    EXEC @ItemID =  _FN_ADD_INITIAL_EQUIP @NewCharID, 10, @RefNeckID, @DurNeck
    IF (@ItemID <= 0) BEGIN
        ROLLBACK TRANSACTION
        RETURN -8
    END
 END
 -- Ring 1
 IF (@RefRingID <> 0) BEGIN
    EXEC @ItemID =  _FN_ADD_INITIAL_EQUIP @NewCharID, 11, @RefRingID, @DurRing
    IF (@ItemID <= 0) BEGIN
        ROLLBACK TRANSACTION
        RETURN -8
    END
 END
 -- Ring 2
 IF (@RefRingID <> 0) BEGIN
    EXEC @ItemID =  _FN_ADD_INITIAL_EQUIP @NewCharID, 12, @RefRingID, @DurRing
    IF (@ItemID <= 0) BEGIN
        ROLLBACK TRANSACTION
        RETURN -8
    END
 END
-----------------------------------------------------------------------------  
 -- default skill넣어주기  
 -----------------------------------------------------------------------------  
 DECLARE @country tinyINT  
 EXEC @country = _GetObjCountry @RefCharID  
   
 INSERT INTO _CharSkillMastery (CharID, MasteryID, Level)  
 SELECT @NewCharID, MasteryID, 0  
 FROM _RefCharDefault_SkillMastery  
 WHERE Race = @country or Race = 3  
 IF (@@error <> 0)  
 BEGIN  
  ROLLBACK TRANSACTION  
  RETURN -13  
 END  
 INSERT INTO _CharSkill (CharID,SkillID,Enable)  
 SELECT @NewCharID, SkillID, 1  
 FROM  _RefCharDefault_Skill  
 WHERE Race = @country or Race = 3  
 IF (@@error <> 0)  
 BEGIN  
  ROLLBACK TRANSACTION  
  RETURN -14  
 END  
 -----------------------------------------------------------------------------  
 -- TutorialQuest넣어주기  
 -----------------------------------------------------------------------------  
 INSERT INTO _CharQuest (CharID, QuestID, Status, AchievementCount, StartTime, EndTime, QuestData1, QuestData2)  
 SELECT @NewCharID, QuestID, 4, 0, getdate(), getdate(), 0, 0  
 FROM _RefCharDefault_Quest  
 WHERE Race = @country or Race = 3  
 IF (@@error <> 0)  
 BEGIN  
  ROLLBACK TRANSACTION  
  RETURN -15  
 END  
 -----------------------------------------------------------------------------  
 -- Static Avatar Initial Record 넣기  
 -----------------------------------------------------------------------------  
 INSERT INTO _StaticAvatar(CharID) values(@NewCharID)  
 IF (@@ERROR <> 0)  
 BEGIN  
  ROLLBACK TRANSACTION  
  RETURN -16  
 END   
  
 -----------------------------------------------------------------------------  
 -- CharList에 ID 넣어주기  
 -----------------------------------------------------------------------------  
 INSERT _CharNameList VALUES(@CharName, @NewCharID)  

--exec _ADD_ITEM_EXTERN @CharName,'ITEM_ETC_E060118_60EXP_HELP',1,1
--exec _ADD_ITEM_EXTERN @CharName,'ITEM_ETC_E060118_100EXP_HELP',1,1
--exec _ADD_ITEM_EXTERN @CharName,'ITEM_ETC_SCROLL_RETURN_NEWBIE_01',50,1
--EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_SHIELD_01_C_RARE',255,12

EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_BLADE_10_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_BOW_10_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_EARRING_10_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_10_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_10_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_10_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_10_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_10_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_10_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_10_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_10_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_10_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_10_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_10_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_10_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_10_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_10_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_10_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_10_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_10_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_10_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_10_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_10_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_10_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_NECKLACE_10_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_RING_10_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_RING_10_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_SHIELD_10_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_SPEAR_10_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_SWORD_10_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_TBLADE_10_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_10_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_10_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_10_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_10_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_10_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_10_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_10_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_10_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_10_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_10_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_10_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_10_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_10_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_10_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_10_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_10_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_10_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_10_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_10_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_10_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_10_SA_C_RARE',255,12


SELECT @temp = count(CharID) FROM _User WITH (NOLOCK) WHERE UserJID = @UserJID
IF (@temp >= 1)  
BEGIN
UPDATE _Char SET RemainGold=100000, RemainSkillPoint=10000000 WHERE _Char.CharID = @NewCharID 
-----
EXEC  _Dkchar @NewCharID
----
DELETE FROM [BR_ACCOUNT].[dbo].[SK_Silk] where JID = @UserJID

INSERT INTO [BR_ACCOUNT].[dbo].[SK_Silk] VALUES (@UserJID,9999,9999,9999)
---
end
 COMMIT TRANSACTION  
  
  
 RETURN @NewCharID