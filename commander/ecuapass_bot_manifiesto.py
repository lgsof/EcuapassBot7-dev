
import os, sys 
import pyautogui as py
import pyperclip
from pyautogui import ImageNotFoundException

from info.ecuapass_exceptions import EcudocBotStopException, EcudocBotCartaporteNotFound, EcudocCloudException
from info.ecuapass_utils import Utils
from info.ecuapass_extractor import Extractor

from ecuapass_bot import EcuBot

#----------------------------------------------------------
# Globals
#----------------------------------------------------------
sys.stdout.reconfigure(encoding='utf-8')

#----------------------------------------------------------
def main ():
	args = sys.argv 
	jsonFilepath = args [1]
	runningDir   = os.getcwd()
	mainBotManifiesto (jsonFilepath, runningDir)

#----------------------------------------------------------
# Main function for testing
#----------------------------------------------------------
def mainBotManifiesto (jsonFilepath, runningDir):
	bot = EcuBotManifiesto (jsonFilepath, runningDir)
	bot.initSettings ()
	message = bot.start ()
	return message
	
#--------------------------------------------------------------------
# self for filling Ecuapass cartaporte web form (in flash)
#--------------------------------------------------------------------
class EcuBotManifiesto (EcuBot):
	def __init__(self, empresa, jsonFilepath, runningDir):
		super().__init__ (empresa, jsonFilepath, runningDir, "MANIFIESTO")

	def fillEcuapass (self):
		# print ("\n>>>>>> Identificacion del Transportista Autorizado <<<")
		py.PAUSE = self.NORMAL_PAUSE
		self.fillBoxWait  ("01_TipoProcedimiento")
		self.fillBoxWait  ("02_Sector")
		self.fillDate     ("03_Fecha_Emision"); py.press ("Tab")
		self.fillBoxIter  (self.fields ["04_Distrito"])
		self.fillText     ("05_MCI")
		py.press ("Tab"); 

		# print (">>> Identificación Permisos")
		[py.press ("left") for i in range (3)]
		if self.fields ["07_TipoPermiso_CI"]:
			pass
		elif self.fields ["08_TipoPermiso_PEOTP"]:
			py.press ("right")
		elif self.fields ["09_TipoPermiso_PO"]:
			if not self.clickPORButton ():
				[py.press ("right") for i in range (3)]
		py.press ("Tab")

		# print ("\n>>>>>> Identificacion del Transportista Autorizado <<<")
		self.fillText     ("10_PermisoOriginario")
		self.fillText     ("11_PermisoServicios1")
		self.fillText     ("12_PermisoServicios2")
		self.fillText     ("13_PermisoServicios3")
		self.fillText     ("14_PermisoServicios4")

		# Transportista Info
		self.fillTransportistaInfo ("15_NombreTransportista", "16_DirTransportista")
		#py.press ("Tab"); #self.fillText     ("15_NombreTransportista")   # Default ECUAPASS value
		#py.press ("Tab"); #self.fillText     ("16_DirTransportista")      # Default ECUAPASS value

		self.scrollN (15)

		# print ("\n>>>>>> Identificacion del Vehículo Habilitado <<<")
		self.fillText     ("17_Marca_Vehiculo")
		self.fillText     ("18_Ano_Fabricacion")
		self.fillBoxWait  ("19_Pais_Vehiculo")
		self.fillText     ("20_Placa_Vehiculo")
		self.fillText     ("21_Nro_Chasis")
		self.fillText     ("22_Nro_Certificado")
		self.fillBoxWait  ("23_Tipo_Vehiculo")

		# print ("\n>>>>>> Identificacion de la Unidad de Carga (Remolque) <<<")
		self.fillText     ("24_Marca_remolque")
		self.fillText     ("25_Ano_Fabricacion")
		self.fillText     ("26_Placa_remolque")
		self.fillBoxWait  ("27_Pais_remolque")
		self.fillText     ("28_Nro_Certificado")
		self.fillText     ("29_Otra_Unidad")

		# +++++++++++++++++++++++++++++++++++++++++
		# print ("\n>>>>>> Identificacion de la Tripulacion <<<")
		self.fillBoxWait  ("30_Pais_Conductor")
		self.fillBoxWait  ("31_TipoId_Conductor")
		self.fillText     ("32_Id_Conductor")
		self.fillBoxWait  ("33_Sexo_Conductor")
		self.fillDate     ("34_Fecha_Conductor"); py.press ("TAB")
		self.fillText     ("35_Nombre_Conductor")
		self.fillText     ("36_Licencia_Conductor")
		self.fillText     ("37_Libreta_Conductor")

		self.fillBoxWait  ("38_Pais_Auxiliar")
		self.fillBoxWait  ("39_TipoId_Auxiliar")
		self.fillText     ("40_Id_Auxiliar")
		self.fillBoxWait  ("41_Sexo_Auxiliar")
		self.fillDate     ("42_Fecha_Auxiliar"); py.press ("Tab")
		self.fillText     ("43_Nombre_Auxiliar")
		self.fillText     ("44_Apellido_Auxiliar")
		self.fillText     ("45_Licencia_Auxiliar")
		self.fillText     ("46_Libreta_Auxiliar")

		#--------------------------------------------------
		# Datos Sobre la Carga
		#--------------------------------------------------
		self.scrollN (12)
		#--------------------------------------------------
		#-- TEST: Fill pais-pais-pais.....ciudad-ciudad-....-ciudad
		py.sleep (self.SLOW_PAUSE)
		self.fillBoxWait      ("47_Pais_Carga"); py.press ('Tab') # Pais carga
		self.fillBoxWait      ("49_Pais_Descarga"); self.skipN (6)  # Pais descarga
		self.fillBoxWait      ("56_Pais"); self.skipN (9, 'LEFT')   # Pais Incoterm
		self.fillBoxWait      ("48_Ciudad_Carga"); py.press ('TAB') 
		self.fillBoxWait      ("50_Ciudad_Descarga")
		self.fillBoxNoDown    ("51_Tipo_Carga")
		self.fillText         ("52_Descripcion_Carga"); 
		self.fillText         ("53_Precio_Mercancias")
		self.fillBoxWait      ("54_Incoterm")
		self.fillBoxWait      ("55_Moneda"); py.press ('TAB')
		self.fillBoxWait      ("57_Ciudad")

		#-- Check selection and Fill Aduana 'destino' 
		if self.fillBoxWait   ("58_AduanaDest_Pais", "NOTAB"):
			py.press ("up"); py.press ("down"); py.press ("Tab")    # To load ECUAPASS DATA
			self.fillBoxWait      ("59_AduanaDest_Ciudad")
		else:
			self.skipN (2)

		self.fillText         ("60_Peso_NetoTotal")
		self.fillText         ("61_Peso_BrutoTotal")
		self.fillText         ("62_Volumen")
		self.fillText         ("63_OtraUnidad"); 
		self.skipN (3)

		#------------------------------------------------------
		# Check selection and set aduanas: 'cruce' and 'destino'
		#------------------------------------------------------
		if self.fillBoxWait ("64_AduanaCruce_Pais", "NOTAB"):
			py.press ("up"); py.press ("down"); py.press ("Tab"); py.sleep (0.1)
			self.fillBoxWait      ("65_AduanaCruce_Ciudad")
			py.press ("space"); py.sleep (0.1); py.press ("space");
			self.skipN (2, "LEFT")

		if self.fillBoxWait ("58_AduanaDest_Pais", "NOTAB"):
			py.press ("up"); py.press ("down"); py.press ("Tab"); py.sleep (0.1)
			self.fillBoxWait      ("59_AduanaDest_Ciudad")
			py.press ("space"); py.sleep (0.1); py.press ("space");
		else:
			self.skipN (2)

		#--------------------------------------------------
		# Datos de Detalle de la Carga
		#--------------------------------------------------
		self.skipN (6)
		self.scrollN (30)

		self.fillText     ("66_Secuencia")
		self.skipN (4)    # Skip Fixed values and Cartaporte
		self.fillText     ("70_TotalBultos")
		self.fillBoxWait  ("71_Embalaje")
		self.fillText     ("72_Marcas")
		self.fillText     ("73_Peso_Neto")
		self.fillText     ("74_Peso_Bruto")
		self.fillText     ("75_Volumen")
		self.fillText     ("76_OtraUnidad")
		self.fillText     ("77_Nro_UnidadCarga")
		self.fillBoxWait ("78_Tipo_UnidadCarga")
		self.fillBoxWait ("79_Cond_UnidadCarga")
		self.fillText     ("80_Tara")
		self.fillText     ("81_Descripcion")

		#--------------------------------------------------
		# Precintos and go back for searching Cartaporte
		#--------------------------------------------------
		if self.fillPrecintos (fieldName="82_Precinto"):
			print (f"+++ Regresando precintos: 17")
			self.skipN (17, "LEFT")          # Go back to Find Button  
		else:
			print (f"+++ Regresando precintos: 13")
			self.skipN (13, "LEFT")          # Go back to Find Button  

		print ("\n>>>>>> Buscando/Seleccionando cartaporte <<<<<<")
		self.searchSelectCartaporte ()

	#--------------------------------------------------------------------
	# Select current, continue if exist info, fill from DB otherwise
	# Send info to Ecuapass Cloud
	#--------------------------------------------------------------------
	def fillTransportistaInfo (self, fieldNombre, fieldDir):
		try:
			# Handle 'nombre'
			pyperclip.copy ("")
			py.hotkey ("ctrl", "a", "c"); py.sleep (0.1)
			nombre = pyperclip.paste().upper().strip()
			Utils.printx (f"+++ fillTransportistaInfo::nombre:  '{nombre}'")

			if nombre:
				py.press ("tab")
			else:
				self.fillText  (fieldNombre)   # Default ECUAPASS value

			# Hangle'direccion'
			pyperclip.copy ("")
			py.hotkey ("ctrl", "a", "c"); py.sleep (0.1)
			direccion = pyperclip.paste().upper().strip()
			if direccion:
				py.press ("tab")
			else:
				self.fillText  (fieldDir)      # Default ECUAPASS value

		except EcudocCloudException as ex:
			raise


	#--------------------------------------------------------------------
	# Add precintos, one by one, to manifiesto
	#--------------------------------------------------------------------
	def fillPrecintos (self, fieldName):
		if not Extractor.getValidValue (self.fields [fieldName]):
			return False
		self.skipN (4)
		try:
			text = self.fields [fieldName].replace (" ","")
			precintosList = text.split (",")
			for p in precintosList:
				print (f"+++ Precinto: '{p}'")
				self.checkStopFlag ()
				py.write (p)
				py.press ("tab"); py.press ("space"); py.press ("space")
				py.hotkey ("shift", "tab")
				py.sleep (0.2)
			return True
		except:
			Utils.printException ("Agregando precintos:", precintosList)
			raise Exception ("No se pudo adicionar los precintos. Adicionelos manualmente")

	#--------------------------------------------------------------------
	# Search and selecte the firs cartaporte from a table of listed cartaportes
	#--------------------------------------------------------------------
	def searchSelectCartaporte (self):
		self.mouseController.release_mouse ()
		py.PAUSE = self.NORMAL_PAUSE
		py.press ("space");  self.waitForInfo (confineMouse=False) # Press Find button
		self.skipN (3);                          # Go to "fecha/hora" and select "Mes" 
		self.fillBoxIter ("Mes", "NO_TAB")
		self.skipN (3); py.press ("end") # Go to "tipo documento" and select "CPIC"
		self.skipN (3); py.press ("space"); 
		py.sleep (0.5); self.waitForInfo (confineMouse=False); # "Consultar CPICs"
		self.skipN (2, "LEFT"); self.fillText     ("69_CPIC", "NO_TAB"); # Fill "Cartaporte" number
		self.skipN (4)                   # Go to found cartaportes
		py.press ("down")
		py.press ("enter")
		self.clickSelectedCartaporte ("69_CPIC")
		py.press ("Tab"); py.press ("space")
		py.PAUSE = self.NORMAL_PAUSE

		self.skipN (13)
		py.press ("space"); py.press ("space")

	#-- Click on selected cartaporte
	def clickSelectedCartaporte (self, fieldName):
		try:
			Utils.printx ("Localizando imagen cartaporte seleccionada...")
			xy = EcuBot.findEcuapassImage ("image-blue-text-terrestre")
			Utils.printx ("...Cartaporte detectada")
			py.click (xy[0], xy[1], interval=1)    
			return
		except ImageNotFoundException as ex:
			Utils.printx ("No se detectó image cartaporte seleccionada")
			raise EcudocBotCartaporteNotFound ()
		finally:
			self.mouseController.release_mouse ()

	#-- Click on Permiso Originario Radio Button
	def clickPORButton (self):
		try:
			self.mouseController.release_mouse ()

			Utils.printx ("Clicking Permiso Originario...")
			filePaths = Utils.getPathImage ("image-rbutton-PermisoOriginario")
			for fpath in filePaths:
				print (">>> Probando: ", os.path.basename (fpath))
				xy = py.locateCenterOnScreen (fpath, confidence=0.70, grayscale=False)
				if (xy):
					Utils.printx ("...RButton detectado")
					py.click (xy[0], xy[1], interval=1)    

					self.mouseController.confine_mouse ()
					return
		except Exception as ex:
			Utils.printException ("No se encontró imágen RBotón de Permiso Originario")

		py.PAUSE = self.FAST_PAUSE

#--------------------------------------------------------------------
# Call to main
#--------------------------------------------------------------------
if __name__ == "__main__":
	main()

