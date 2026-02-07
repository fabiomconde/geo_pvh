class LimitePVH(models.Model):
    """Limite Municipal de Porto Velho (Sem distritos)"""
    gid = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, default='Porto Velho')
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        managed = True
        db_table = 'geo"."limite_pvh'
        verbose_name = 'Limite de Porto Velho'
        verbose_name_plural = 'Limites de Porto Velho'

    def __str__(self):
        return self.nome
