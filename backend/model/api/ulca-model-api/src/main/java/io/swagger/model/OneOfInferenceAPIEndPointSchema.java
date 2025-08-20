package io.swagger.model;


import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;

/**
* OneOfInferenceAPIEndPointSchema
*/
@JsonTypeInfo(
  use = JsonTypeInfo.Id.NAME,
		  include = JsonTypeInfo.As.PROPERTY, 
property = "taskType"
)
@JsonSubTypes({
	  @JsonSubTypes.Type(value = TranslationInference.class, name = "translation"),
	  @JsonSubTypes.Type(value = TransliterationInference.class, name = "transliteration"),
	  @JsonSubTypes.Type(value = ASRInference.class, name = "asr"),
	  @JsonSubTypes.Type(value = TTSInference.class, name = "tts"),
	  @JsonSubTypes.Type(value = OCRInference.class, name = "ocr"),
	  @JsonSubTypes.Type(value = TxtLangDetectionInference.class, name = "txt-lang-detection"),
	  @JsonSubTypes.Type(value = NerInference.class, name = "ner"),
	  @JsonSubTypes.Type(value = AudioGenderDetectionInference.class, name = "audio-gender-detection"),
	  @JsonSubTypes.Type(value = AudioLangDetectionInference.class, name = "audio-lang-detection"),
	  @JsonSubTypes.Type(value = ITNInference.class, name = "itn"),
	  @JsonSubTypes.Type(value = TNInference.class, name = "text-normalization"),
	  @JsonSubTypes.Type(value = ImgLangDetectionInference.class, name = "img-lang-detection")
	})
public interface OneOfInferenceAPIEndPointSchema {

}
