import os
from dataclasses import dataclass
from typing import Any
@dataclass(slots=True)
class AIModelLoadResult:
    model: Any = None
    model_found: bool = False
    error_message: str | None = None
class AILoader:
    def __init__(self, context_or_config):
        if hasattr(context_or_config, "base_dir") and hasattr(context_or_config, "config_AI"):
            self.config = context_or_config
        else: self.config = context_or_config.config
        self.base_dir = self.config.base_dir
    def _get_selected_training(self) -> str:
        training = next((key for key, value in self.config.config_AI["type_training"].items() if value), None)
        if training is None: raise ValueError("No se especifico un tipo de entrenamiento valido.")
        return training
    def _get_selected_model(self) -> str:
        model = next((key for key, value in self.config.config_AI["type_model"].items() if value), None)
        if model is None: raise ValueError("No se especifico un tipo de modelo valido.")
        return model
    def _get_hidden_architecture(self) -> list[int]:
        nn_cfg = self.config.config_AI.get("nn", {"hidden_layers": 2, "neurons_per_layer": 6})
        neurons = nn_cfg.get("neurons_per_layer", 6)
        layers = nn_cfg.get("hidden_layers", 2)
        return [neurons] * layers
    def _resolve_loader(self):
        training = self._get_selected_training()
        model_type = self._get_selected_model()
        arch = self._get_hidden_architecture()
        if training == "Genetic":
            from src.Type_Training.Genetic_Algorithm import load_genetic_model
            return load_genetic_model, (model_type, 6, 2), {"hidden_sizes": arch}
        if training == "Q-learning":
            from src.Type_Training.Q_learning import load_qlearning_model
            return load_qlearning_model, (model_type, 6, 2), {"hidden_sizes": arch}
        raise ValueError(f"Tipo de entrenamiento no soportado: {training}")
    def load_model_result(self) -> AIModelLoadResult:
        model_path = os.path.join(self.base_dir, "AI", "best_model.pth")
        try:
            load_callable, args, kwargs = self._resolve_loader()
            if not os.path.exists(model_path):
                return AIModelLoadResult(model=None, model_found=False, error_message=None)
            model = load_callable(model_path, *args, **kwargs)
            if model is None:
                return AIModelLoadResult(
                    model=None,
                    model_found=False,
                    error_message="No se pudo cargar el modelo guardado.",)
            return AIModelLoadResult(model=model, model_found=True, error_message=None)
        except Exception as exc:
            return AIModelLoadResult(model=None, model_found=False, error_message=str(exc))
    def load_model(self):
        return self.load_model_result().model