
import sys
import pyautogui as py
from info.ecuapass_utils import Utils
from ecuapass_bot import EcuBot

#----------------------------------------------------------
# Globals
#----------------------------------------------------------
sys.stdout.reconfigure(encoding='utf-8')
PAUSE = 0

def main ():
	import os
	args = sys.argv 
	ecuFieldsFilepath = args [1]
	runningDir   = os.getcwd()
	mainBotCartaporte (ecuFieldsFilepath, runningDir)

#----------------------------------------------------------
# Main function for testing
#----------------------------------------------------------
def mainBotCartaporte (ecuFieldsFilepath, runningDir):
	bot = EcuBotCartaporte (ecuFieldsFilepath, runningDir)
	bot.initSettings ()
	message = bot.start ()
	return message
	
#--------------------------------------------------------------------
# self for filling Ecuapass cartaporte web form (in flash)
#--------------------------------------------------------------------
class EcuBotCartaporte (EcuBot):
	def __init__(self, empresa, ecuFieldsFilepath, runningDir):
		super().__init__ (empresa, ecuFieldsFilepath, runningDir, "CARTAPORTE")

	#-- Bot document typing
	def fillEcuapass (self):
		# Encabezado
		self.fillBoxIter (self.fields ["01_Distrito"])
		self.fillText ("02_NumeroCPIC")
		self.fillText ("03_MRN")

		self.fillText ("04_MSN"); py.sleep (0.1)
		self.fillBoxWait ("05_TipoProcedimiento")
		#self.fillBoxWait ("06_EmpresaTransporte") # Selected by default
		py.press ("Tab")
		self.fillBoxWait ("07_DepositoMercancia", "TAB_NOCHECK")

		self.fillText ("08_DirTransportista")
		self.fillText ("09_NroIdentificacion")

		self.scrollN (13)

		# Remitente
		self.fillSubject ("REMITENTE", "05_TipoProcedimiento", "10_PaisRemitente", 
						  "11_TipoIdRemitente", "12_NroIdRemitente", "14_NombreRemitente",
						  "15_DireccionRemitente", "13_NroCertSanitario")

		# Destinatario
		self.fillSubject ("DESTINATARIO", "05_TipoProcedimiento", "16_PaisDestinatario",
						  "17_TipoIdDestinatario", "18_NroIdDestinatario", 
						  "19_NombreDestinatario", "20_DireccionDestinatario")
		# Consignatario
		self.fillSubject ("CONSIGNATARIO", "05_TipoProcedimiento", "21_PaisConsignatario", 
						  "22_TipoIdConsignatario", "23_NroIdConsignatario", 
						  "24_NombreConsignatario", "25_DireccionConsignatario")

		self.scrollN (10)

		# Notificado
		self.fillText ("26_NombreNotificado")
		self.fillText ("27_DireccionNotificado")
		self.fillBoxWait ("28_PaisNotificado")

		# Paises y fechas: Recepcion, Embarque, Entrega
		self.fillBoxWait ("29_PaisRecepcion"); self.skipN (2)
		self.fillBoxWait ("32_PaisEmbarque"); self.skipN (2)
		self.fillBoxWait ("35_PaisEntrega"); 
		self.skipN (12); py.sleep (0.2)
		self.fillBoxWait ("48_PaisMercancia"); # Pais INCOTERM
		self.skipN (13); py.sleep (0.1)
		self.fillBoxWait ("62_PaisEmision"); py.sleep (0.1)

		# Go back to fill other fields
		#self.skipN (34, "LEFT"); py.press ("Tab"); py.sleep (0.1); 
		self.skipN (33, "LEFT"); py.sleep (0.5); 
		self.fillBoxWait ("30_CiudadRecepcion"); 
		self.fillDate     ("31_FechaRecepcion"); self.skipN (2)
		self.fillBoxWait ("33_CiudadEmbarque"); 
		self.fillDate     ("34_FechaEmbarque"); self.skipN (2)
		self.fillBoxWait ("36_CiudadEntrega"); 
		self.fillDate     ("37_FechaEntrega"); py.press ("Tab")
		# Condiciones
		self.fillBoxWait ("38_CondicionesTransporte")
		self.fillBoxWait ("39_CondicionesPago")
		# Mercancia

		py.PAUSE = self.FAST_PAUSE
		self.fillText     ("40_PesoNeto")
		self.fillText     ("41_PesoBruto")
		self.fillText     ("42_TotalBultos")
		self.fillText     ("43_Volumen")
		self.fillText     ("44_OtraUnidad")
		self.fillText     ("45_PrecioMercancias")
		# INCOTERM
		py.PAUSE = self.NORMAL_PAUSE
		self.fillBoxWait ("46_INCOTERM")
		self.fillBoxWait ("47_TipoMoneda"); py.press ("Tab")
		# Ciudad INCOTERM
		self.fillBoxWait ("49_CiudadMercancia")

		# Gastos
		self.fillText     ("50_GastosRemitente")
		self.fillBoxWait ("51_MonedaRemitente")
		self.fillText     ("52_GastosDestinatario")
		self.fillBoxWait ("53_MonedaDestinatario")
		self.fillText     ("54_OtrosGastosRemitente")
		self.fillBoxWait ("55_OtrosMonedaRemitente")
		self.fillText     ("56_OtrosGastosDestinatario")
		self.fillBoxWait ("57_OtrosMonedaDestinataio")
		self.fillText     ("58_TotalRemitente")
		self.fillText     ("59_TotalDestinatario")
		# Documentos
		self.fillText     ("60_DocsRemitente")
		# Emision
		self.fillDate     ("61_FechaEmision"); py.press ("Tab"); py.press ("Tab")
		self.fillBoxWait ("63_CiudadEmision")

		# Instrucciones
		self.scrollN (14)
		self.fillText ("64_Instrucciones")
		self.fillText ("65_Observaciones")

		self.skipN (3)

		# Detalles
		self.fillText     ("66_Secuencia")
		self.fillText     ("67_TotalBultos")
		self.fillBoxWait ("68_Embalaje")
		self.fillText     ("69_Marcas")
		self.fillText     ("70_PesoNeto")
		self.fillText     ("71_PesoBruto")
		self.fillText     ("72_Volumen")
		self.fillText     ("73_OtraUnidad")

		# IMOs
		self.fillText     ("74_Subpartida"); py.press ("Tab")
		self.fillBoxWait ("75_IMO1")
		self.fillBoxWait ("76_IMO2")
		self.fillBoxWait ("77_IMO2")
		self.fillText     ("78_NroCertSanitario")
		self.fillText     ("79_DescripcionCarga")

		# Valid RUC ID with find button in 'Remitente', 'Destinatario', 'Consignatario'
		#if "IMPORTACION" in self.fields ["05_TipoProcedimiento"]:
			
		message = "Cartaporte digitada"
		return message

	#--------------------------------------------------------------------
	# Fill subject fields waiting for RUC info for ecuadorian companies
	#--------------------------------------------------------------------
	def fillSubject (self, subjectType, fieldProcedimiento, fieldPais, fieldTipoId, 
					 fieldNumeroId, fieldNombre, fieldDireccion, fieldCertificado=None):
		#---------------- fill data about subject -------------------
		def fillData (fieldPais, fieldTipoId, fieldNumeroId):
			self.fillBoxCheck (fieldPais)
			self.fillBoxCheck (fieldTipoId)
			self.fillText (fieldNumeroId)
		#------------------------------------------------------------
		self.checkStopFlag ()
		procedimiento = self.fields [fieldProcedimiento]
		Utils.printx (f"Procedimiento: '{procedimiento}', Sujeto: '{subjectType}'")
		fillData (fieldPais, fieldTipoId, fieldNumeroId); py.sleep (0.05)

		if self.fields [fieldPais] == "ECUADOR" and self.fields [fieldTipoId] == "RUC":
			Utils.printx ("Es una empresa ecuatoriana, verificando RUC")
			nTries = 0
			delay = 0.0
			while nTries < 3:
				self.checkStopFlag ()
				Utils.printx ("...Esperando botón de búsqueda")
				if self.isOnFindButton (): 
					break
				self.skipN (3, "LEFT")
				fillData (fieldPais, fieldTipoId, fieldNumeroId); py.sleep (0.05 + delay)
				nTries +=1
				delay += 0.02
				
			if nTries == 4:
				raise EcudocEcuapassException (f"BOTERROR::No se pudo transmitir datos de sujeto '{subjectType}'")

			py.press ("space"); 
			py.sleep (1)
			self.waitForInfo ()
		else:
			Utils.printx ("No es una empresa ecuatoriana, no verifica RUC")
			if subjectType == "REMITENTE":
				self.fillText (fieldCertificado)
			self.fillText (fieldNombre)

		self.fillText (fieldDireccion)

#----------------------------------------------------------
#----------------------------------------------------------
if __name__ == "__main__":
	main()


