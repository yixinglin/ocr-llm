from tortoise import fields, Tortoise, run_async
from tortoise.models import Model

class T_BizProduct(Model):
    id = fields.IntField(pk=True)
    create_by = fields.CharField(max_length=50, null=True)
    create_time = fields.DatetimeField(null=True)
    update_by = fields.CharField(max_length=50, null=True)
    update_time = fields.DatetimeField(null=True)
    name = fields.CharField(max_length=200, null=True)
    article_number = fields.CharField(max_length=64, unique=True, null=True)
    unit = fields.CharField(max_length=64, null=True)
    price_clsa = fields.FloatField(null=True)
    price_clsb = fields.FloatField(null=True)
    catg_id = fields.IntField(null=True)
    link_url = fields.CharField(max_length=256, null=True)
    images = fields.TextField(null=True)
    intro = fields.TextField(null=True)
    note_img = fields.CharField(max_length=256, null=True)
    relate_field1 = fields.CharField(max_length=16, null=True)
    relate_field2 = fields.CharField(max_length=16, null=True)
    note_file = fields.CharField(max_length=1024, null=True)
    min_quantity = fields.IntField(default=1)
    seq_no = fields.IntField(default=1)
    deleted = fields.BooleanField(default=False)
    status = fields.CharField(max_length=2, default='0')

    class Meta:
        table = "biz_product"

