from resemblyzer import VoiceEncoder,preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st


@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()

def get_voice_embedding(audio_bytes):
    try:
        encoder=load_voice_encoder()
        
        audio,sr=librosa.load(io.BytesIO(audio_bytes),sr=16000) #A sampling rate of 16,000 means 16,000 audio samples are taken every second.
        wav=preprocess_wav(audio) #prepares that audio for Resemblyzer
        embedding=encoder.embed_utterance(wav) #Resemblyzer produces a 256-dimensional voice embedding
        
        return embedding.tolist() #It is converted to list ,since it favourable in storing it in databases and send through API etc
    
    except Exception as e:
        st.error("Voice recognition error")
        return None



def identify_speaker(new_embedding,candidates_dict,threshold=0.65):
    if new_embedding is None or not candidates_dict:
        return None,0.0
    
    best_sid=None
    best_score=-1.0
    
    for sid,stored_embedding in candidates_dict.items():
        if stored_embedding:
            similarity=np.dot(new_embedding,stored_embedding)
            if similarity>best_score:      #Higher the similarity ,higher is the chance of that person's voice
                best_score=similarity 
                best_sid=sid
                
    
    if best_score>=threshold:
        return best_sid,best_score
    
    else:
        None,best_score
    

def process_bulk_audio(audio_bytes,candidate_dict,threshold=0.65):
    
    try:
        encoder=load_voice_encoder()
        audio,sr=librosa.load(io.BytesIO(audio_bytes),sr=16000)
        
        segments=librosa.effects.split(audio,top_db=30)      #Split the audio since many students would be saying present ,top_db too high means only stu screaming present will get registered and too low will result in attendace of student whispering
        
        
        identified_results={}
        
        for start,end in segments:
            if (end-start) < sr*0.5:    # Get rid of garbage noises
                continue
            
            segment_audio=audio[start:end]
            wav=preprocess_wav(segment_audio)
            embedding=encoder.embed_utterance(wav)
            
            sid,score=identify_speaker(embedding,candidate_dict,threshold)
            
            if sid:
                if sid not in identify_speaker or score>identified_results[sid]:
                    identified_results[sid]=score
                    
        
        return identified_results
    
    except Exception as e:
        st.error("Bulk process error")
        return {}

