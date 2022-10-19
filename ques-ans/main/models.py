from __future__ import unicode_literals
from py2neo import Graph,Node,Relationship
from django.db import models
from neo4j.v1 import GraphDatabase, basic_auth

# Create your models here.
class Neo4j():
	driver = None
	neo4j_db = None
	def __init__(self):
		print("create neo4j class ...")
	def connectDB(self):
		uri = "bolt://localhost:7687"
		# self.driver = GraphDatabase.driver(uri, auth=("neo4j", "123456nba"))
		print("okma")
		self.driver = GraphDatabase.driver(uri, auth=("neo4j", "1207044910"))
		print("ok")
		return self.driver



# -----------------------------------------------------------------------------------------------------




# # This is an auto-generated Django model module.
# # You'll have to do the following manually to clean this up:
# #   * Rearrange models' order
# #   * Make sure each model has one field with primary_key=True
# #   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
# #   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# # Feel free to rename the models, but don't rename db_table values or field names.
# from django.db import models
#
#
# class 专利(models.Model):
#     专利名称 = models.CharField(max_length=255)
#     专利类型 = models.CharField(max_length=255, blank=True, null=True)
#     申请公布号 = models.CharField(max_length=255)
#     申请公布日 = models.CharField(max_length=255, blank=True, null=True)
#     申请号 = models.CharField(max_length=255)
#
#     class Meta:
#         managed = True  # 修改为True表示可以对数据库进行修改
#         db_table = '专利'
#
#
# class 人物_copy1(models.Model):
#     人名 = models.CharField(max_length=20, blank=True, null=True)
#     简介 = models.CharField(max_length=1000, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '人物_copy1'
#
#
# class 人物公司_copy1(models.Model):
#     姓名 = models.CharField(max_length=250, blank=True, null=True)
#     公司 = models.CharField(max_length=250, blank=True, null=True)
#     关系 = models.CharField(max_length=250, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '人物公司_copy1'
#
#
# class 作品著作权(models.Model):
#     作品名称 = models.CharField(max_length=255, blank=True, null=True)
#     作品类别 = models.CharField(max_length=255, blank=True, null=True)
#     创作完成日期 = models.CharField(max_length=255, blank=True, null=True)
#     登记号 = models.CharField(max_length=255, blank=True, null=True)
#     登记日期 = models.CharField(max_length=255, blank=True, null=True)
#     首次发表日期 = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '作品著作权'
#
#
# class 公司_copy1(models.Model):
#     名称 = models.CharField(max_length=250, blank=True, null=True)
#     电话 = models.CharField(max_length=250, blank=True, null=True)
#     地址 = models.CharField(max_length=1500, blank=True, null=True)
#     邮箱 = models.CharField(max_length=1500, blank=True, null=True)
#     网址 = models.CharField(max_length=1500, blank=True, null=True)
#     注册资本 = models.CharField(max_length=500, blank=True, null=True)
#     成立日期 = models.CharField(max_length=500, blank=True, null=True)
#     经营状态 = models.CharField(max_length=250, blank=True, null=True)
#     工商注册号 = models.CharField(max_length=500, blank=True, null=True)
#     统一社会信用代码 = models.CharField(max_length=500, blank=True, null=True)
#     组织机构代码 = models.CharField(max_length=500, blank=True, null=True)
#     纳税人识别号 = models.CharField(max_length=500, blank=True, null=True)
#     公司类型 = models.TextField(blank=True, null=True)
#     营业期限 = models.CharField(max_length=500, blank=True, null=True)
#     行业 = models.TextField(blank=True, null=True)
#     审核日期 = models.CharField(max_length=1500, blank=True, null=True)
#     人员规模 = models.CharField(max_length=250, blank=True, null=True)
#     实缴资本 = models.CharField(max_length=1500, blank=True, null=True)
#     参保人数 = models.CharField(max_length=250, blank=True, null=True)
#     注册地址 = models.TextField(blank=True, null=True)
#     登记机关 = models.CharField(max_length=500, blank=True, null=True)
#     英文名称 = models.CharField(max_length=1500, blank=True, null=True)
#     经营范围 = models.TextField(blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '公司_copy1'
#
#
# class 公司与公司_copy1(models.Model):
#     投资企业 = models.CharField(max_length=250, blank=True, null=True)
#     被投资企业名称 = models.CharField(max_length=250, blank=True, null=True)
#     投资数额 = models.CharField(max_length=250, blank=True, null=True)
#     投资比例 = models.CharField(max_length=250, blank=True, null=True)
#     经营状态 = models.CharField(max_length=250, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '公司与公司_copy1'
#
#
# class 公司产品(models.Model):
#     作品 = models.CharField(max_length=255, blank=True, null=True)
#     公司 = models.CharField(max_length=255, blank=True, null=True)
#     关系 = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '公司产品'
#
#
# class 公司风险(models.Model):
#     公司 = models.CharField(max_length=255, blank=True, null=True)
#     风险 = models.CharField(max_length=255, blank=True, null=True)
#     关系 = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '公司风险'
#
#
# class 司法风险(models.Model):
#     发布日期 = models.CharField(max_length=255, blank=True, null=True)
#     案件名称 = models.CharField(max_length=255, blank=True, null=True)
#     案件身份 = models.CharField(max_length=255, blank=True, null=True)
#     案号 = models.CharField(max_length=255, blank=True, null=True)
#     案由 = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '司法风险'
#
#
# class 开庭公告(models.Model):
#     公诉人 = models.CharField(max_length=255, blank=True, null=True)
#     开庭日期 = models.CharField(max_length=255, blank=True, null=True)
#     案号 = models.CharField(max_length=255, blank=True, null=True)
#     案由 = models.CharField(max_length=255, blank=True, null=True)
#     被告人 = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '开庭公告'
#
#
# class 法院公告(models.Model):
#     上诉方 = models.CharField(max_length=255, blank=True, null=True)
#     公告类型 = models.CharField(max_length=255, blank=True, null=True)
#     刊登日期 = models.CharField(max_length=255, blank=True, null=True)
#     法院 = models.CharField(max_length=255, blank=True, null=True)
#     被诉方 = models.CharField(max_length=255, blank=True, null=True)
#     id = models.CharField(primary_key=True, max_length=255)
#
#     class Meta:
#         managed = True
#         db_table = '法院公告'
#
#
# class 软件著作权(models.Model):
#     分类号 = models.CharField(max_length=255, blank=True, null=True)
#     版本号 = models.CharField(max_length=255, blank=True, null=True)
#     登记号 = models.CharField(max_length=255, blank=True, null=True)
#     登记批准日期 = models.CharField(max_length=255, blank=True, null=True)
#     软件全称 = models.CharField(max_length=255, blank=True, null=True)
#     软件简称 = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '软件著作权'
