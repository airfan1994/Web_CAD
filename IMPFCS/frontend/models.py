# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100, default='')
    MALE = '男'
    FEMALE = '女'
    GENDER_CHOICES = (
        (MALE, '男'),
        (FEMALE, '女')
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='')
    MISSING = ''
    JIXIE = '机械系',
    RENENG = '热能系',
    DIANJI = '电机系',
    DIANZI = '电子系',
    JISUANJI = '计算机系',
    ZIDONGHUA = '自动化系',
    DEP_CHOICES = (
        (MISSING, ''),
        (JIXIE, '机械系'),
        (RENENG, '热能系'),
        (DIANJI, '电机系'),
        (DIANZI, '电子系'),
        (JISUANJI, '计算机系'),
        (ZIDONGHUA, '自动化系'),
    )
    department = models.CharField(max_length=10, choices=DEP_CHOICES, default=MISSING)
    studentClass = models.CharField(max_length=6, default='')
    
    is_teamMember = models.BooleanField(default=False)
    is_applyingTeam = models.BooleanField(default=False)
    applyTeamTime = models.DateTimeField(null=True)
    A = 'A'
    B = 'B'
    C = 'C'
    TEAMCATEGORY_CHOICES = (
        (MISSING, ''),
        (A, 'A'),
        (B, 'B'),
        (C, 'C'),
    )
    teamCategory = models.CharField(max_length=1, choices=TEAMCATEGORY_CHOICES, default=MISSING)
    TEAMLEADER = '队长'
    LEAGUESECRETARY = '团支书'
    MAMBER = '队员'
    TEAMROLE_CHOICES = (
        (MISSING, ''),
        (TEAMLEADER, '队长'),
        (LEAGUESECRETARY, '团支书'),
        (MAMBER, '队员')
    )
    teamName = models.CharField(max_length=50, default='')
    teamRole = models.CharField(max_length=5, choices=TEAMROLE_CHOICES, default=MISSING)
    coach = models.CharField(max_length=10, default='')
    birth = models.DateField(null=True)
    QUNZHONG = '群众'
    TUANYUAN = '共青团员'
    JIJIFENZI = '积极分子'
    YUBEIDANGYUAN = '预备党员'
    DANGYUAN = '党员'
    PB_CHOICES = (
        (MISSING, ''),
        (QUNZHONG, '群众'),
        (TUANYUAN, '共青团员'),
        (JIJIFENZI, '积极分子'),
        (YUBEIDANGYUAN, '预备党员'),
        (DANGYUAN, '党员'),
    )
    politicalBackground = models.CharField(max_length=4, choices=PB_CHOICES, default=MISSING)
    #GPA_Rank = models.CharField(max_length=100, default='')  #json
    GPA_Rank = [models.CharField(max_length=100, default=''), models.CharField(max_length=100, default='')]
    phoneNum = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=50, default='')
    work = models.CharField(max_length=400, default='')

    @staticmethod
    def fields():
        return set(BasicInfo._meta.get_all_field_names()).difference({'user', 'user_id', 'id'})


 
