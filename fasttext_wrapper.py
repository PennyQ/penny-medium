"""
The mlflow.models module provides an API for saving machine learning models in "flavors" that can be understood by different downstream tools.
However, FastText is not yet being supported. Thus, we use generic mlflow.pyfunc module to create a wrapper for FastText models. 
This util file is aiming to bridge this gap. 
"""

import fasttext
import mlflow.pyfunc


class FastTextWrapper(mlflow.pyfunc.PythonModel):
    """
    Class to train and use FastText Models
    """

    def load_context(self, context):
        """This method is called when loading an MLflow model with pyfunc.load_model(), as soon as the Python Model is constructed.

        Args:
            context: MLflow context where the model artifact is stored.
        """
        import fasttext

        self.model = fasttext.load_model(context.artifacts["fasttext_model_path"])

    def predict(self, context, model_input):
        """This is an abstract function. We customized it into a method to fetch the FastText model.

        Args:
            context ([type]): MLflow context where the model artifact is stored.
            model_input ([type]): the input data to fit into the model.

        Returns:
            [type]: the loaded model artifact.
        """
        return self.model


def save_model(
    df: pd.DataFrame,
    model_name: str = "model_name",
    corpus_filename: str = "prepared_corpus",
    prepared_content: str = "prepared_text",
):
    """
    Runs the Skipgram model using the corpus created and saved by the 'prepare_corpus' function, saves the model and
    returns the trained model. The output of this function is a trained model in binary file format stored as an
    artifact in MLflow tracking server.

    Args:
        df (pd.DataFrame): Dataframe with text content
        model_name (str): Model will be saved with this name as a .bin file
        corpus_filename (str, optional): Name of the .txt file of the corpus. Defaults to 'prepared_corpus'.
        prepared_content (str, optional): Column name for prepared text. Defaults to 'prepared_text'.

    Returns:
        trained_model: Returns the trained model
    """
    prepare_corpus(df, corpus_filename, prepared_content)
    trained_model = fasttext.train_unsupervised(
        corpus_filename + ".txt", model="skipgram", dim=50, ws=10, epoch=400
    )

    fasttext_model_path = model_name + ".bin"
    trained_model.save_model(fasttext_model_path)

    artifacts = {"fasttext_model_path": fasttext_model_path}
    mlflow_pyfunc_model_path = model_name

    with mlflow.start_run() as run:
        mlflow.pyfunc.log_model(
            artifact_path=mlflow_pyfunc_model_path,
            python_model=FastTextWrapper(),
            code_path=["./your_code_path"],
            artifacts=artifacts,
        )

    return trained_model


def load_model(self, model_name: str = "model_name", stage: str = "Production"):
    """
    Loads the trained fasttext (Skipgram) model from the DSPE and returns
    it as mlflow.pyfunc.PyFuncModel to be used to do the predictions.
    IMPORTANT: The function returns the MLflow model, not the predictions.
    """
    loaded_model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{stage}")

    # Use the abstract function in FastTextWrapper to fetch the trained model.
    # TODO: this solution can be improved by implement the whole predict part into the wrapper function.
    fasttext_model = loaded_model.predict(pd.DataFrame([1, 2, 3]))

    self.logger.info("Type of the model is")
    self.logger.info(type(fasttext_model))

    return fasttext_model
