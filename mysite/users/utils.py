from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.utils.text import slugify


def generate_unique_slug(base_slug, instance_pk=None, model_cls=None):
    """
    根據 base_slug 嘗試生成唯一的 slug。
    :param base_slug: 來源的 slug（例如 username、full_name）
    :param instance_pk: 若為更新狀況，傳入原物件的 pk 排除自己
    :param model_cls: 要查詢的 Model 類別（預設為 Profile）
    :return: 唯一的 slug 字串
    :raises ValidationError: 若無法生成唯一值
    """
    """生成唯一的 slug。"""
    from users.models import Profile
    if model_cls is None:
        model_cls = Profile
    slug = slugify(base_slug)
    for _ in range(10):
        slug = f"{base_slug}-{get_random_string(10)}"
        qs = model_cls.objects.filter(slug=slug)
        if instance_pk:
            qs = qs.exclude(pk=instance_pk)
        if not qs.exists():
            return slug
    raise ValidationError("無法生成唯一的網址，請再試一次或使用不同網址")


def mask_name(name: str) -> str:
    length = len(name)
    if length == 1:
        result = "Ｏ"
    elif length == 2:
        result = name[0] + "Ｏ"
    else:
        result = name[0] + "Ｏ" * (length - 2) + name[-1]
    return result
