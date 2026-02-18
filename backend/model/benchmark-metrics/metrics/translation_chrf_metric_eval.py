import logging
from logging.config import dictConfig
from models.model_metric_eval import ModelMetricEval
from datasets import load_metric
import numpy as np
import os

log = logging.getLogger('file')


class TranslationChrfScoreEval(ModelMetricEval):
    """
    Implementation of metric evaluation of Translation type models
    using ChrF.

    ChrF is an MT evaluation metric that uses the F-score statistic
    for character n-gram matches.
    """

    def __init__(self):
        # self.chrf_score = load_metric('chrf', revision='master')
        chrf_path = os.path.join(os.path.dirname(__file__), 'chrf')
        self.chrf_score = load_metric(chrf_path)

    def machine_translation_metric_eval(self, ground_truth, machine_translation, language):
        try:
            if not ground_truth or not machine_translation:
                return None

            if len(ground_truth) != len(machine_translation):
                log.error("Ground truth and prediction length mismatch")
                return None

            # 🔥 Force flatten nested lists completely
            def flatten_text_list(data):
                flattened = []
                for item in data:
                    if isinstance(item, list):
                        if len(item) > 0:
                            flattened.append(str(item[0]))
                        else:
                            flattened.append("")
                    else:
                        flattened.append(str(item))
                return flattened

            ground_truth = flatten_text_list(ground_truth)
            machine_translation = flatten_text_list(machine_translation)

            # Debug (optional – remove after verification)
            log.info(f"GT sample type: {type(ground_truth[0])}")
            log.info(f"MT sample type: {type(machine_translation[0])}")

            eval_score = self.chrf_score.compute(
                predictions=machine_translation,
                references=ground_truth,
                lowercase=True
            )

            score = eval_score.get("score")

            if score is None or np.isnan(score):
                log.error("Unable to calculate chrf score for translation")
                return None

            return score

        except Exception as e:
            log.exception(f"Exception in calculating chrf: {str(e)}")
            return None


# Log configuration
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] {%(filename)s:%(lineno)d} %(threadName)s %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'info': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'filename': 'info.log'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {
        'file': {
            'level': 'DEBUG',
            'handlers': ['info', 'console'],
            'propagate': False
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['info', 'console']
    }
})
