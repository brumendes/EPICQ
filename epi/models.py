from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

import datetime
from dateutil.relativedelta import relativedelta


# Create your models here.

class Sala(models.Model):
    nome = models.CharField(max_length=50)
    abreviatura = models.CharField(max_length=10)

    def __str__(self):
        return "%s" % self.nome


class Tipo(models.Model):
    nome = models.CharField(max_length=50)
    abreviatura = models.CharField(max_length=10)

    def __str__(self):
        return "%s" % self.nome


class Tamanho(models.Model):
    designacao = models.CharField(max_length=5)

    def __str__(self):
        return "%s" % self.designacao


class EspessuraPb(models.Model):
    valor = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "EspessurasPb"

    def __str__(self):
        return "%s" % self.valor


class EPI(models.Model):
    STATE_CHOICES = (
        ("Activo", "Activo"),
        ("Inactivo", "Inactivo"),
        ("Pendente", "Pendente"),
    )
    GENERO_CHOICES = (
        ("M", "M"),
        ("F", "F"),
    )
    UTILIZACAO_CHOICES = {
        ("Intensiva", "Intensiva"),
        ("Frequente", "Frequente"),
        ("Rara", "Rara"),
    }
    estado = models.CharField(max_length=30, choices=STATE_CHOICES, default="Activo")
    data_alteracao = models.DateTimeField(auto_now=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name="epis_sala")
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, related_name="epis_tipo")
    marca = models.CharField(max_length=30, null=True, blank=True)
    modelo = models.CharField(max_length=30, null=True, blank=True)
    cor = models.CharField(max_length=30, null=True, blank=True)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE, related_name="epis_tamanho", null=True, blank=True)
    genero = models.CharField(max_length=2, choices=GENERO_CHOICES, null=True, blank=True)
    referencia = models.CharField(max_length=20, null=True, blank=True)
    espessuraPb = models.ForeignKey(EspessuraPb, on_delete=models.CASCADE, related_name="epis_espessuraPb", null=True,
                                    blank=True)
    utilizacao = models.CharField(max_length=20, choices=UTILIZACAO_CHOICES, null=True, blank=True)
    norma = models.CharField(max_length=20, null=True, blank=True)
    data = models.DateField(null=True, blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "EPI's"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())
        super(EPI, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('epi:epi_detail', kwargs={'slug': self.slug})

    def get_latest_ver(self):
        if self.verif_epis.exists():
            latest_ver = self.verif_epis.order_by('data').latest()
        else:
            latest_ver = None
        return latest_ver

    def get_state(self):
        latest_ver = self.get_latest_ver()
        summary = latest_ver.get_summary()
        return summary

    def get_ver_frequency(self):
        if self.utilizacao == "Intensiva":
            frequency = "8 meses"
        elif self.utilizacao == "Frequente":
            frequency = "16 meses"
        elif self.utilizacao == "Rara":
            frequency = "2 anos"
        else:
            frequency = ""
        return frequency

    def get_frequency_text(self):
        if self.utilizacao == "Intensiva":
            frequency_text = ">3h/dia"
        elif self.utilizacao == "Frequente":
            frequency_text = ">3h/semana"
        else:
            frequency_text = ""
        return frequency_text

    def get_next_ver(self):
        latest_ver = self.get_latest_ver()
        if latest_ver:
            start_date = latest_ver.data
            if self.utilizacao == "Intensiva":
                next_ver = start_date + relativedelta(months=+8)
            elif self.utilizacao == "Frequente":
                next_ver = start_date + relativedelta(months=+16)
            elif self.utilizacao == "Rara":
                next_ver = start_date + relativedelta(months=+24)
            else:
                next_ver = ''
        else:
            next_ver = ''
        return next_ver

    def __str__(self):
        return "%s %s" % (self.tipo.abreviatura, self.pk)


class Verificacao(models.Model):
    CONSERVACAO_CHOICES = {
        ("Novo", "Novo"),
        ("Bom estado de conservação", "Bom estado de conservação"),
        ("Desgaste externo. Malha intacta.", "Desgaste externo. Malha intacta."),
        ("Fissura sem importância.", "Fissura sem importância."),
        ("Fissura em local crítico.", "Fissura em local crítico."),
    }
    LIMPEZA_CHOICES = {
        ("Limpo", "Limpo"),
        ("Sangue", "Sangue"),
        ("Contraste", "Contraste"),
        ("Sangue + contraste", "Sangue + contraste"),
    }
    CONFORME_CHOICES = (
        (None, "N/D"),
        (True, "Sim"),
        (False, "Não"),
    )
    epi = models.ForeignKey(EPI, on_delete=models.CASCADE, related_name="verif_epis")
    sala = models.ForeignKey(Sala, null=True, blank=True, on_delete=models.CASCADE)
    acondicionamento = models.NullBooleanField(choices=CONFORME_CHOICES)
    conservacao = models.CharField(max_length=300, choices=CONSERVACAO_CHOICES)
    fitavelcro = models.NullBooleanField(choices=CONFORME_CHOICES)
    limpeza = models.CharField(max_length=300, choices=LIMPEZA_CHOICES)
    data = models.DateField(auto_now_add=True)
    utilizador = models.CharField(max_length=100, null=True, blank=True)
    obs = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Verificações"
        get_latest_by = 'data'

    def get_summary(self):
        if self.acondicionamento == "Não" or self.conservacao == "Fissura em local crítico." or not (
                self.limpeza == "Limpo") or self.fitavelcro == "Não":
            summary = "Com defeito"
        else:
            summary = "OK"
        return summary

    def get_absolute_url(self):
        return reverse('epi:verif_detail', kwargs={'slug': self.epi.slug, 'pk': self.pk})

    def __str__(self):
        return '%s %s' % (self.epi, self.data)


class Image(models.Model):
    verificacao = models.ForeignKey(Verificacao, on_delete=models.CASCADE, related_name='imagens')
    image = models.ImageField(null=True, blank=True, upload_to="media")

    def __str__(self):
        return '%s %s' % (self.verificacao.epi, self.verificacao.data)
