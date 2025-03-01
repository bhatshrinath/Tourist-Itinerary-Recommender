import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

from pyspark.ml.recommendation import ALS
from sklearn.neighbors import NearestNeighbors

import tensorflow as tf
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model


# 1. Restricted Boltzmann Machine (RBM) Model
class RBM:
    """
    Restricted Boltzmann Machine (RBM) model for collaborative filtering.

    Parameters:
        visible_units (int): The number of visible units.
        hidden_units (int): The number of hidden units.

    Attributes:
        visible_units (int): The number of visible units.
        hidden_units (int): The number of hidden units.
        model (tf.keras.Model): The RBM model.
    """

    def __init__(self, visible_units, hidden_units):
        self.visible_units = visible_units
        self.hidden_units = hidden_units
        self.model = self.build_model()

    def build_model(self):
        input_layer = Input(shape=(self.visible_units,))
        hidden = Dense(self.hidden_units, activation="relu")(input_layer)
        output_layer = Dense(self.visible_units, activation="sigmoid")(hidden)
        model = Model(inputs=input_layer, outputs=output_layer)
        model.compile(optimizer="adam", loss="binary_crossentropy")
        return model

    def train(self, X, epochs=10, batch_size=32):
        self.model.fit(X, X, epochs=epochs, batch_size=batch_size, verbose=1)


# 2. Alternating Least Squares (ALS) Model
class ALSModel:
    """
    Alternating Least Squares (ALS) model for collaborative filtering.

    Parameters:
        spark (pyspark.sql.SparkSession): The Spark session.
        rank (int): The number of latent factors.
        maxIter (int): The maximum number of iterations.
        regParam (float): The regularization parameter.

    Attributes:
        spark (pyspark.sql.SparkSession): The Spark session.
        rank (int): The number of latent factors.
        maxIter (int): The maximum number of iterations.
        regParam (float): The regularization parameter.
        model (pyspark.ml.recommendation.ALSModel): The ALS model.
    """

    def __init__(self, spark, rank=10, maxIter=10, regParam=0.1):
        self.spark = spark
        self.rank = rank
        self.maxIter = maxIter
        self.regParam = regParam
        self.model = None

    def train(self, hotel_spark_df):
        als = ALS(
            userCol="user_id",
            itemCol="hotel_id",
            ratingCol="rating",
            rank=self.rank,
            maxIter=self.maxIter,
            regParam=self.regParam,
        )
        self.model = als.fit(hotel_spark_df)


# 3. K-Means Clustering Model
class HotelClustering:
    """
    K-Means clustering model for hotel data.

    Parameters:
        n_clusters (int): The number of clusters.
        random_state (int): The random seed.

    Attributes:
        n_clusters (int): The number of clusters.
        random_state (int): The random seed.
        kmeans (sklearn.cluster.KMeans): The KMeans model.
    """

    def __init__(self, n_clusters=3, random_state=42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=self.random_state)

    def fit(self, data):
        return self.kmeans.fit(data)


# 4. K-Nearest Neighbors (KNN) for Memory-Based Filtering
class HotelRecommenderKNN:
    """
    K-Nearest Neighbors (KNN) model for hotel recommendations.

    Parameters:
        n_neighbors (int): The number of neighbors.
        metric (str): The distance metric.

    Attributes:
        n_neighbors (int): The number of neighbors.
        metric (str): The distance metric.
        knn (sklearn.neighbors.NearestNeighbors): The KNN model.
    """

    def __init__(self, n_neighbors=5, metric="cosine"):
        self.n_neighbors = n_neighbors
        self.metric = metric
        self.knn = NearestNeighbors(n_neighbors=self.n_neighbors, metric=self.metric)

    def fit(self, data):
        self.knn.fit(data)

    def recommend_hotels(self, hotel_id, hotel_df, k=5):
        index = hotel_df[hotel_df["hotel_id"] == hotel_id].index[0]
        distances, indices = self.knn.kneighbors(
            [hotel_df.iloc[index, 1:].values], n_neighbors=k + 1
        )
        return hotel_df.iloc[indices[0][1:], :]


def train_models(
    rbm_units=(5, 3),
    als_params=(10, 10, 0.1),
    kmeans_clusters=3,
    knn_neighbors=5,
    train=False,
):
    """
    Train the recommender models. This function initializes the RBM, ALS, KMeans, and KNN models.

    Parameters:
        rbm_units (tuple): The number of visible and hidden units for RBM.
        als_params (tuple): The rank, maxIter, and regParam for ALS.
        kmeans_clusters (int): The number of clusters for KMeans.
        knn_neighbors (int): The number of neighbors for KNN.

    Returns:
        tuple: A tuple of trained models (RBM, ALSModel, HotelClustering, HotelRecommenderKNN).
    """
    if train:
        rbm = RBM(visible_units=rbm_units[0], hidden_units=rbm_units[1])
        als_model = ALSModel(
            spark=None,
            rank=als_params[0],
            maxIter=als_params[1],
            regParam=als_params[2],
        )
        hotel_clustering = HotelClustering(n_clusters=kmeans_clusters)
        hotel_knn = HotelRecommenderKNN(n_neighbors=knn_neighbors)
        return rbm, als_model, hotel_clustering, hotel_knn
    else:
        pass
