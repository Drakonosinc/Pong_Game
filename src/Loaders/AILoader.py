import os
from Type_Training.Genetic_Algorithm import load_genetic_model
from Type_Training.Q_learning import load_qlearning_model
class AILoader:
    def __init__(self, context):
        self.config = context.config
        self.base_dir = self.config.base_dir
    def load_model(self):
        model_path = os.path.join(self.base_dir, "AI/best_model.pth")
        nn_cfg = self.config.config_AI.get("nn", {"hidden_layers": 2, "neurons_per_layer": 6})
        neurons = nn_cfg.get("neurons_per_layer", 6)
        layers = nn_cfg.get("hidden_layers", 2)
        arch = [neurons] * layers
        type_training = next((k for k, v in self.config.config_AI["type_training"].items() if v), None)
        type_model = next((k for k, v in self.config.config_AI["type_model"].items() if v), None)
        model_training = None
        if os.path.exists(model_path):
            try:
                if type_training == "Genetic": 
                    model_training = load_genetic_model(model_path, type_model, 6, 2, hidden_sizes=arch)
                    print(f"Modelo Genético cargado desde: {model_path}")
                elif type_training == "Q-learning": 
                    model_training = load_qlearning_model(model_path, type_model, 6, 2, hidden_sizes=arch)
                    print(f"Modelo Q-Learning cargado desde: {model_path}")
            except Exception as e: print(f"Error cargando el modelo: {e}")
        return model_training