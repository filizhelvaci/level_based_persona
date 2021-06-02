 #############################################
# PROJE: LEVEL BASED PERSONA TANIMLAMA, BASIT SEGMENTASYON ve KURAL TABANLI SINIFLANDIRMA
#############################################

# Hedefimiz tekil olarak var olan müşteriler için önce gruplandırmalar yapmak (level based persona tanımlama)
# sonra da bu grupları segmentlere ayırmaktır.
# Son olarak da yeni gelebilecek bir müşterinin bu segmentlerden hangisine ait olduğunu belirlemeye çalışmaktır.

import pandas as pd
pd.set_option('display.float_format', lambda x: '%.3f' % x)

users=pd.read_csv('hafta2/users.csv')
purchases=pd.read_csv('hafta2/purchases.csv')

# veri setlerini birleştiriyoruz(uid'lere göre merge ediyoruz)
df=users.merge(purchases,on="uid")
df.shape
df.head()

# country,device,gender,age değişkenlerine göre groupby'a alıp,price'ın sum'ını alıyoruz
df.groupby(["country","device","gender","age"])[["price"]].sum()

# agg_df 'e azalan sıralayarak kaydediyoruz
agg_df=df.groupby(["country","device","gender","age"]).agg({"price":"sum"}).sort_values("price",ascending=False)
agg_df.head()

# index'i değişken olarak çıkarıyoruz
agg_df=agg_df.reset_index()

# age'den kategorik olan age_cat değişkenini tanımlıyoruz
agg_df["age_cat"] = pd.cut(x=agg_df["age"], bins=[0,19,25,45,60,agg_df["age"].max()],labels=['0_18','19_24','25_44','45_59','60_'+str(agg_df["age"].max())])

# age değişkenini uçuruyoruz
agg_df=agg_df.drop("age",axis=1)

# level based persona için isimleri oluşturuyoruz
customers_level_based=[row[0]+"_"+row[1].upper()+"_"+row[2]+"_"+row[4] for row in agg_df.values]
# isimleri agg_df'e tanımlıyoruz
agg_df["customers_level_based"]=customers_level_based
# kaç isim tanımlanmış sayısını alıyoruz
agg_df["customers_level_based"].count() #450

# tanımlanan isimlere göre price'ların ortalamasını alıyoruz
dff=agg_df.groupby("customers_level_based").agg({"price":"mean"})
dff=dff.reset_index()

# customers_level_persona'yı segmentlere ayırıyoruz
a=pd.qcut(dff["price"],4,labels=["D", "C", "B", "A"])
dff["groups"]=a
dff.reset_index(drop=True,inplace=True)
dff.groupby("groups").agg({"price":"mean"})

dff[dff["customers_level_based"] == "TUR_IOS_F_25_44"]

