#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 09:31:27 2022
Modifié le 15 mai 2024

@author: Moi, ou pas. Du moins pas totalement.
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from scipy.io.wavfile import write
from scipy.io import wavfile
import wave
import time
import pyaudio #faut creer une variable d'environnement virtuel avec py 3.13

plt.close('all')

############################################################################
def spectre(signal:np.ndarray)->np.ndarray:
    """ la fonction permet de calculer le spectre du signal d'entrée
        parametres : signal dont on souhaite le spectre
        retour : spectre du signal
    """
    Fourier = 2/(len(signal))*np.fft.fftshift(np.fft.fft(signal,2*len(signal))) # 2* en test
    Module = np.abs(Fourier)
    Module1=Module[int(len(Module)/2):len(Module)]
    return Module1

def affichage(x:np.ndarray, signal:np.ndarray, titre:str)->None:
    """ la fonction permet d'afficher la courbe dont les paramètres sont donnés en entrée
        parametres : 
            x : vecteur des abcisses
            signal : signal à afficher
            titre : titre de la courbe
    """
    plt.figure()
    plt.plot(x,signal)
    plt.grid()
    if x[len(x)-1]<100:
        plt.xlabel("temps en s", fontsize=14)
    else :
        plt.xlabel("fréquence en Hz ", fontsize=14)
    plt.ylabel("Amplitude en V", fontsize=14)
    plt.title(titre, fontsize=16)
    plt.show()


def filtre(ordre:int, fc, typef:str, entree:np.ndarray )->np.ndarray:
    """ la focntion permet de filter le signal avec un filtre Butterworth
        parametres :
            ordre : ordre du Butterworth
            fc : fréquence(s) de coupeure du filtre
                si typef = "band" alors =[fcb, fch] ou fcb = fréquence basse et fch = fréquence haute
            typef : type de filtre :
                law : passe bas
                high : passe haut
                band : passe band
        retour :
            signal de sortie du filtre
    """
    if typef=="band":
        fcb=fc[0]/(fe/2)
        fch=fc[1]/(fe/2)
        b, a = scipy.signal.butter(ordre, [fcb,fch], btype=typef, analog=False)
        w, h = scipy.signal.freqz(b, a)
        f=0.5 * fe * w / np.pi
        fig, ax = plt.subplots(1,1, figsize = (15, 10))
        plt.grid()    
        ax.semilogx(f[1:len(f)-1], 20*np.log10(abs(h[1:len(f)-1])),linewidth = 2)
        ax.set_xlim([10,fe/2])
        ax.set_ylim([-65,5])
        ax.xaxis.set_tick_params(labelsize=12)
        ax.yaxis.set_tick_params(labelsize=12)
        ax.set_title("Gain en dB du filtre", fontsize=16)
        ax.set_xlabel("Fréquence, échelle semilog", fontsize=14)
        ax.set_ylabel("20log|G| en dB", fontsize=14)
        ax.grid(True, which="both")
        
        #Notation de la fréquence de coupure à -3dB
        ax.vlines(x=fc[0], ymin=-65, ymax=-3, colors='g',linestyles="dashed")
        ax.vlines(x=fc[1], ymin=-65, ymax=-3, colors='g',linestyles="dashed")
        ax.hlines(y=-3, xmin=1, xmax=fc[1], colors='g',linestyles="dashed")
        #ax.text(8.5, -5.5, 'G à fc', fontsize=16)
    
    else :
        fcn=fc/(fe/2)
        b, a = scipy.signal.butter(ordre, fcn, btype=typef, analog=False)
        w, h = scipy.signal.freqz(b, a)
        f=0.5 * fe * w / np.pi
        fig, ax = plt.subplots(1,1, figsize = (15, 10))
        plt.grid()    
        ax.semilogx(f[1:len(f)-1], 20*np.log10(abs(h[1:len(f)-1])),linewidth = 2)
        ax.set_xlim([10,fe/2])
        ax.set_ylim([-65,5])
        ax.xaxis.set_tick_params(labelsize=12)
        ax.yaxis.set_tick_params(labelsize=12)
        ax.set_title("Gain en dB du filtre", fontsize=16)
        ax.set_xlabel("Fréquence, échelle semilog", fontsize=14)
        ax.set_ylabel("20log|G| en dB", fontsize=14)
        ax.grid(True, which="both")
        
        #Notation de la fréquence de coupure à -3dB
        ax.vlines(x=fc, ymin=-65, ymax=-3, colors='g',linestyles="dashed")
        ax.hlines(y=-3, xmin=1, xmax=fc, colors='g',linestyles="dashed")
        #ax.text(8.5, -5.5, 'G à fc', fontsize=16)

    #Gère l'espacement vertical entre les 2 systèmes d'axes
    fig.tight_layout()
    out=scipy.signal.lfilter(b, a, entree)
    return out

def play_audio_file(nom_fichier_wave:str)->None:
    """ la fonction permet de jouer le son d'un fichier wave
        parametres : nom du ficier wave
    """
    ding_wav = wave.open(nom_fichier_wave, "rb")
    ding_data = ding_wav.readframes(ding_wav.getnframes())
    audio = pyaudio.PyAudio()
    stream_out = audio.open(
        format=audio.get_format_from_width(ding_wav.getsampwidth()),
        channels=ding_wav.getnchannels(),
        rate=ding_wav.getframerate(), input=False, output=True)
    stream_out.start_stream()
    stream_out.write(ding_data)
    time.sleep(0.2)
    stream_out.stop_stream()
    stream_out.close()
    audio.terminate()
#############################################################################
if __name__ == "__main__":
    # declaration des variaboles :
    fe:np.int_ = 32000 # fréquence echantillionnage
    T:float# 0.005 # termps d'observation
    t:np.ndarray # vecteur temps
    f:np.ndarray # vecteur fréquence
    fich_entree:str # nom du fichier entree
    fich_sortie:str # nom du fichier de sortie
    
    # initialisation
    fich_entree = "Quentin.wav"
    fe, mod = wavfile.read(fich_entree)
    #T : float = 5.802625
    #T = len(mod)
    T = len(mod)/fe
    t = np.linspace(start=0,stop=T-1/fe,num=int(T*fe))
    #f = np.linspace(start=0, stop= fe/2-1/len(mod),num=int(T*fe/2)+1)
    f = np.linspace(start=0, stop= fe/2-1/len(mod),num=int(len(mod)))

    # exemple lecture fichier wave
    #write("test.wav", fe, out)
    
    mod=mod/1390000000
    
    #play_audio_file(fich_entree)


    # Pour afficher le signal modulant en fonction du temps t
    #affichage(t, mod, 'Signal temporel')

    # Pour afficher le signal modulant en fonction de la frequence f
    #affichage(f, mod, 'Signal fréquentiel')

    # Pour filtrer le signal
    mod_filtre=filtre(1, [1, 3000], 'band', mod)
    #affichage(f,mod_filtre,'Signal filtré')
    #affichage(f,spectre(mod_filtre),'Spectre du signal')

    # Mise en place de la fréquence porteuse
    porteuse = np.cos(2*np.pi*4800*t)
    #affichage(t, porteuse, 'Signal temporel de la porteuse')
    #affichage(f, spectre(porteuse), 'Signal fréquentiel de la porteuse')

    # Modulation du signal
    module = mod * porteuse
    #affichage(t, module, 'Signal temporel du signal modulé')
    #affichage(f, module, 'Signal fréquentiel du signal modulé')
    #affichage(f, spectre(module), 'Spectre fréquentiel du signal modulé')

    # Démodulation du signal
    demodule = module * porteuse
    #affichage(t, demodule, 'Signal temporel du signal démodulé')
    #affichage(f, demodule, 'Signal fréquentiel du signal démodulé')
    #affichage(f, spectre(demodule), 'Spectre fréquentiel du signal démodulé')

    # Filtrage du son final
    final = filtre(1, [1, 3000], 'band', demodule)
    #affichage(t, final, 'Signal temporel du signal final')
    #affichage(f, final, 'Signal fréquentiel du signal final')
    #affichage(f, spectre(final), 'Spectre fréquentiel du signal final')


    # Export du signal 
    write("test.wav", fe, final)

