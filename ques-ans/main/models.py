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
# class ר��(models.Model):
#     ר������ = models.CharField(max_length=255)
#     ר������ = models.CharField(max_length=255, blank=True, null=True)
#     ���빫���� = models.CharField(max_length=255)
#     ���빫���� = models.CharField(max_length=255, blank=True, null=True)
#     ����� = models.CharField(max_length=255)
#
#     class Meta:
#         managed = True  # �޸�ΪTrue��ʾ���Զ����ݿ�����޸�
#         db_table = 'ר��'
#
#
# class ����_copy1(models.Model):
#     ���� = models.CharField(max_length=20, blank=True, null=True)
#     ��� = models.CharField(max_length=1000, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '����_copy1'
#
#
# class ���﹫˾_copy1(models.Model):
#     ���� = models.CharField(max_length=250, blank=True, null=True)
#     ��˾ = models.CharField(max_length=250, blank=True, null=True)
#     ��ϵ = models.CharField(max_length=250, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '���﹫˾_copy1'
#
#
# class ��Ʒ����Ȩ(models.Model):
#     ��Ʒ���� = models.CharField(max_length=255, blank=True, null=True)
#     ��Ʒ��� = models.CharField(max_length=255, blank=True, null=True)
#     ����������� = models.CharField(max_length=255, blank=True, null=True)
#     �ǼǺ� = models.CharField(max_length=255, blank=True, null=True)
#     �Ǽ����� = models.CharField(max_length=255, blank=True, null=True)
#     �״η������� = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '��Ʒ����Ȩ'
#
#
# class ��˾_copy1(models.Model):
#     ���� = models.CharField(max_length=250, blank=True, null=True)
#     �绰 = models.CharField(max_length=250, blank=True, null=True)
#     ��ַ = models.CharField(max_length=1500, blank=True, null=True)
#     ���� = models.CharField(max_length=1500, blank=True, null=True)
#     ��ַ = models.CharField(max_length=1500, blank=True, null=True)
#     ע���ʱ� = models.CharField(max_length=500, blank=True, null=True)
#     �������� = models.CharField(max_length=500, blank=True, null=True)
#     ��Ӫ״̬ = models.CharField(max_length=250, blank=True, null=True)
#     ����ע��� = models.CharField(max_length=500, blank=True, null=True)
#     ͳһ������ô��� = models.CharField(max_length=500, blank=True, null=True)
#     ��֯�������� = models.CharField(max_length=500, blank=True, null=True)
#     ��˰��ʶ��� = models.CharField(max_length=500, blank=True, null=True)
#     ��˾���� = models.TextField(blank=True, null=True)
#     Ӫҵ���� = models.CharField(max_length=500, blank=True, null=True)
#     ��ҵ = models.TextField(blank=True, null=True)
#     ������� = models.CharField(max_length=1500, blank=True, null=True)
#     ��Ա��ģ = models.CharField(max_length=250, blank=True, null=True)
#     ʵ���ʱ� = models.CharField(max_length=1500, blank=True, null=True)
#     �α����� = models.CharField(max_length=250, blank=True, null=True)
#     ע���ַ = models.TextField(blank=True, null=True)
#     �Ǽǻ��� = models.CharField(max_length=500, blank=True, null=True)
#     Ӣ������ = models.CharField(max_length=1500, blank=True, null=True)
#     ��Ӫ��Χ = models.TextField(blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '��˾_copy1'
#
#
# class ��˾�빫˾_copy1(models.Model):
#     Ͷ����ҵ = models.CharField(max_length=250, blank=True, null=True)
#     ��Ͷ����ҵ���� = models.CharField(max_length=250, blank=True, null=True)
#     Ͷ������ = models.CharField(max_length=250, blank=True, null=True)
#     Ͷ�ʱ��� = models.CharField(max_length=250, blank=True, null=True)
#     ��Ӫ״̬ = models.CharField(max_length=250, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '��˾�빫˾_copy1'
#
#
# class ��˾��Ʒ(models.Model):
#     ��Ʒ = models.CharField(max_length=255, blank=True, null=True)
#     ��˾ = models.CharField(max_length=255, blank=True, null=True)
#     ��ϵ = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '��˾��Ʒ'
#
#
# class ��˾����(models.Model):
#     ��˾ = models.CharField(max_length=255, blank=True, null=True)
#     ���� = models.CharField(max_length=255, blank=True, null=True)
#     ��ϵ = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '��˾����'
#
#
# class ˾������(models.Model):
#     �������� = models.CharField(max_length=255, blank=True, null=True)
#     �������� = models.CharField(max_length=255, blank=True, null=True)
#     ������� = models.CharField(max_length=255, blank=True, null=True)
#     ���� = models.CharField(max_length=255, blank=True, null=True)
#     ���� = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '˾������'
#
#
# class ��ͥ����(models.Model):
#     ������ = models.CharField(max_length=255, blank=True, null=True)
#     ��ͥ���� = models.CharField(max_length=255, blank=True, null=True)
#     ���� = models.CharField(max_length=255, blank=True, null=True)
#     ���� = models.CharField(max_length=255, blank=True, null=True)
#     ������ = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '��ͥ����'
#
#
# class ��Ժ����(models.Model):
#     ���߷� = models.CharField(max_length=255, blank=True, null=True)
#     �������� = models.CharField(max_length=255, blank=True, null=True)
#     �������� = models.CharField(max_length=255, blank=True, null=True)
#     ��Ժ = models.CharField(max_length=255, blank=True, null=True)
#     ���߷� = models.CharField(max_length=255, blank=True, null=True)
#     id = models.CharField(primary_key=True, max_length=255)
#
#     class Meta:
#         managed = True
#         db_table = '��Ժ����'
#
#
# class �������Ȩ(models.Model):
#     ����� = models.CharField(max_length=255, blank=True, null=True)
#     �汾�� = models.CharField(max_length=255, blank=True, null=True)
#     �ǼǺ� = models.CharField(max_length=255, blank=True, null=True)
#     �Ǽ���׼���� = models.CharField(max_length=255, blank=True, null=True)
#     ���ȫ�� = models.CharField(max_length=255, blank=True, null=True)
#     ������ = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = '�������Ȩ'
