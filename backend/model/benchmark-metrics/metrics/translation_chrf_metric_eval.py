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
        chrf_path = os.path.join(os.path.dirname(__file__), 'chrf')
        self.chrf_score = load_metric(chrf_path)

    def machine_translation_metric_eval(self, ground_truth, machine_translation, language):
        try:
            if not ground_truth or not machine_translation:
                return None

            if len(ground_truth) != len(machine_translation):
                log.error("Ground truth and prediction length mismatch")
                return None

            # 🔥 Flatten nested lists
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

            # ✅ Apply lowercase manually (since metric doesn't support it)
            ground_truth = [text.lower() for text in ground_truth]
            machine_translation = [text.lower() for text in machine_translation]

            # Debug logs
            log.info(f"GT sample type: {type(ground_truth[0])}")
            log.info(f"MT sample type: {type(machine_translation[0])}")

            # ✅ Removed lowercase=True
            eval_score = self.chrf_score.compute(
                predictions=machine_translation,
                references=ground_truth
            )

            # ✅ Handle both possible keys safely
            score = eval_score.get("score") or eval_score.get("chrf")

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