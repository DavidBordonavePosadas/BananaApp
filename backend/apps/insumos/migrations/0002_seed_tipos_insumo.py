from django.db import migrations

TIPOS = [
    "Bolsas",
    "Diésel",
    "Hilos",
    "Periódicos",
    "Abono",
    "Fungicida",
    "Mantenimiento",
    "Otros",
]


def seed_tipos(apps, schema_editor):
    TipoInsumo = apps.get_model("insumos", "TipoInsumo")
    for nombre in TIPOS:
        TipoInsumo.objects.get_or_create(nombre=nombre)


def unseed_tipos(apps, schema_editor):
    TipoInsumo = apps.get_model("insumos", "TipoInsumo")
    TipoInsumo.objects.filter(nombre__in=TIPOS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("insumos", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_tipos, reverse_code=unseed_tipos),
    ]
