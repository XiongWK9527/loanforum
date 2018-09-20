CREATE TABLE `t_kanong` (
  `Id` bigint(20) NOT NULL AUTO_INCREMENT,
  `pid` varchar(256) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT '产品id',
  `name` varchar(512) CHARACTER SET utf8 DEFAULT '' COMMENT '产品名称',
  `edu` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '额度',
  `description` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '产品描述',
  `feiyong` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '费用',
  `applyNum` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '申请人数',
  `qixian` varchar(512) CHARACTER SET utf8 DEFAULT '' COMMENT '期限',
  `fangkuangsudu` varchar(512) CHARACTER SET utf8 DEFAULT '' COMMENT '放款速度',
  `shenhefangshi` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '审核方式',
  `daozhangfangshi` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '到账方式',
  `zhengxi` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '征信要求',
  `platform` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '平台名称',
  `createTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='51卡农';


CREATE TABLE `t_wangdaijin` (
  `Id` bigint(20) NOT NULL AUTO_INCREMENT,
  `pid` varchar(256) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT '产品id',
  `name` varchar(512) CHARACTER SET utf8 DEFAULT '' COMMENT '产品名称',
  `ptime` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '产品时间',
  `phone` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '电话',
  `category` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '类别',
  `edu` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '额度',
  `qixian` varchar(512) CHARACTER SET utf8 DEFAULT '' COMMENT '期限',
  `feiyong` varchar(512) CHARACTER SET utf8 DEFAULT '' COMMENT '费用',
  `shenhefangshi` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '审核方式',
  `fangkuangsudu` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '放款速度',
  `huankuanfangshi` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '还款方式',
  `daozhangfangshi` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '到账方式',
  `shijidaokuang` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '实际到账',
  `xuyaoziliao` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '需要资料',
  `createTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='网贷金';


CREATE TABLE `t_zxwk` (
  `Id` bigint(20) NOT NULL AUTO_INCREMENT,
  `pid` varchar(256) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT '产品id',
  `name` varchar(512) CHARACTER SET utf8 DEFAULT '' COMMENT '产品名称',
  `edu` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '额度',
  `qixian` varchar(512) CHARACTER SET utf8 DEFAULT '' COMMENT '期限',
  `feiyong` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '费用',
  `fangkuangsudu` varchar(512) CHARACTER SET utf8 DEFAULT '' COMMENT '放款速度',
  `shenhefangshi` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '审核方式',
  `daozhangfangshi` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '到账方式',
  `platform` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '平台名称',
  `product` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '产品',
  `phone` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '电话',
  `zhengxi` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '征信要求',
  `shijidaokuang` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '实际到账',
  `category` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '类别',
  `xuyaoziliao` varchar(512) CHARACTER SET utf8 DEFAULT NULL COMMENT '需要资料',
  `createTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='众鑫玩卡';