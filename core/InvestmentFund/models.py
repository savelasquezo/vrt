from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

lst_ranks = (('Silver','Silver'),('Gold','Gold'),('Platinum','Platinum'))
lst_sts = (('Pendiente','Pendiente'),('Aprobado','Aprobado'),('Denegado','Denegado'),('Error','Error'))
lst_banks = (('Binance','Binance'),('Skrill','Skrill'),('PayPal','PayPal'))

FEE = 6000
ATICKETS = 3
MINAMMOUNT = 100000

class Usuario(AbstractUser):
    """
    Custom user model inherited from abstractly user.
    "InvestmentFund/settings.py"
    AUTH_USER_MODEL = 'InvestmentFund.Usuario'
    USERNAME_FIELD = 'username'
    """

    username_validator = UnicodeUsernameValidator()
    
    id = models.AutoField(primary_key=True, verbose_name="id")

    codigo = models.CharField(_("Codigo"),max_length=64 ,unique=True,
                help_text=_("Codigo Impreso en las Credenciales"))
    
    username = models.CharField(_("Usuario"),max_length=64,unique=True, validators=[username_validator],
                help_text=_("Caracters Max-64, Únicamente letras, dígitos y @/./+/-/_"),
                error_messages={"unique": _("¡Usuario Actualmente en Uso!"),},)

    is_active = models.BooleanField(_(" "),default=False)

    is_operating = models.BooleanField(_("Activo"),default=False,
                help_text=_("El Usuario actualmente genera Intereses ¡Posterior a la Fecha de Expiracion sera desactivado!"),)
    
    fee = models.PositiveBigIntegerField(_("Fee"),blank=True,default=0,
                help_text=_("Capital Acumulado en Fee ($COP)"),)

    available_tickets = models.IntegerField(_("Tickets"),blank=True,default=ATICKETS,
                help_text=_("Tickets Disponibles"),)

    full_name = models.CharField(_("Nombre/Apellido"), max_length=64, blank=True)
    email = models.EmailField(_("E-mail"), blank=True)
    phone = models.CharField(_("Telefono"), max_length=64, blank=True)
    
    country = models.CharField(_("Ubicacíon"),max_length=64,blank=True)
    
    ammount = models.PositiveBigIntegerField(_("Inversion"),blank=True,default=0,
                help_text=_("Volumen de Capital Invertido ($COP)"),)
    
    bank = models.CharField(_("Banco"), max_length=32, choices=lst_banks,blank=True,
                help_text=_("Banco/Fundacion o Metodo al cual se realizaran los pagos."),)
    
    bank_account = models.CharField(_("Cuenta-Ahorros"), max_length=32,blank=True,)

    user_rank = models.CharField(_("Categoria"), choices=lst_ranks, default="r1", max_length=16,
                help_text=_("Categoria del Inversionista en VRT"),)
    
    interest = models.DecimalField(_("Interes"), max_digits=5, decimal_places=2, blank=True,default=0,
                help_text=_("Volumen de Retorno Mensual (%)"),)

    date_joined = models.DateTimeField(_("Ingreso"), default=timezone.now)
    date_expire = models.DateTimeField(_("Finaliza"), default=timezone.now)
    
    available = models.PositiveBigIntegerField(_("Acumulado"),blank=True,default=0,
                help_text=_("$Disponible Generado en Intereses"),)
    
    paid = models.PositiveBigIntegerField(_("Abonado"),blank=True,default=0,
                help_text=_("$Abonado al Cliente"),)

    total_interest = models.PositiveBigIntegerField(_("Total"),blank=True,default=0,
                help_text=_("$Total Generado en Intereses"),)

    ref_available = models.PositiveBigIntegerField(_("Acumulado Ref"),blank=True,default=0,
                help_text=_("$Disponible Generado de Comiciones"),)

    ref_paid = models.PositiveBigIntegerField(_("Abonado Ref"),blank=True,default=0,
                help_text=_("$Abonado de Comiciones"),)

    total_ref = models.PositiveBigIntegerField(_("Total Ref"),blank=True,default=0,
                help_text=_("$Total Generado de Comiciones"),)

    total = models.PositiveBigIntegerField(_("Total"),blank=True,default=0,
                help_text=_("$Total Generado ($COP)"),)

    ref_id = models.CharField(_("Credencial del Referido"), max_length=32, blank=True)
    ref_name = models.CharField(_("Nombre/Apellido"), max_length=64, blank=True)
    ref_interest = models.DecimalField(_("Interes"), max_digits=5, decimal_places=2, blank=True,default=0,
        help_text=_("Comisiones Mensuales x Referido (%)"),)

    ref_total = models.PositiveBigIntegerField(_("Total"),blank=True,default=0,
                help_text=_("Capital Generado al Referido ($COP)"),)

    
    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")


class Tickets(models.Model):
        
    id = models.AutoField(primary_key=True, verbose_name="Ticket")
    username = models.ForeignKey(Usuario, on_delete=models.CASCADE,verbose_name="Usuario")
    tAmmount = models.PositiveBigIntegerField(_("Volumen"),blank=False,null=False,default=0,
        help_text=_("Volumen de Capital Solicitado ($COP)"),)

    tAmmountFrom = models.CharField(_("Origen"), max_length=32,blank=False,null=False,
        help_text=_("Origen del Volumen"),)
    
    tBank = models.CharField(_("Banco"), max_length=32,blank=False,null=False,
        help_text=_("Banco/Fundacion o Metodo al cual se realizaran los pagos."))
    
    tBankAccount = models.CharField(_("#Cuenta"), max_length=32,blank=False,null=False)
    
    date = models.DateTimeField(_("Fecha"), default=timezone.now)
    
    tBankTicket = models.CharField(_("Voucher"), max_length=32,blank=True,
        help_text=_("Referencia/Voucher Transaccion"))

    rState = models.CharField(_("Estado"), choices=lst_sts, default="Pendiente", max_length=16)
    
    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")

    def __str__(self):
        return "Ticket: %s" % (self.pk)

class UserRank(models.Model):
        
    rName = models.CharField(_("Categoria"), choices=lst_ranks, max_length=16, unique=True, default="r1",
                                help_text=_("Categoria del Inversionista en VaorTrading"),)
    
    rTravelGift = models.BooleanField(_("Viajes"),)
    rVacations = models.BooleanField(_("Vacaciones"),)
    rGiftCard = models.BooleanField(_("Tarjetas"),)
    rSimCard = models.BooleanField(_("Simcard"),)
    rAdvisory = models.BooleanField(_("Asesorias"),)
    
    class Meta:
            verbose_name = _("Categoria")
            verbose_name_plural = _("Categorias")

    def __str__(self):
        return "Categoria: %s" % (self.rName())