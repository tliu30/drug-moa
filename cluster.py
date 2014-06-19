import sklearn.cluster as skcluster

def k_means(x, n, **kwargs)
    """
    Scalable, but req's even cluster size, not too many clusts
    """
    centroids, labels, inertia = skcluster.k_means(x, n, **kwargs)
    return labels

def affinity_propagation(x, **kwargs):
    """
    NOT scalable, but allows for many clusters & uneven size
    Uses a nearest neighbor graph.

    Uses SIMILARITY matrix
    Consider adding option to set bandwidth
    """
    S = np.ones(x.shape) - x 
    cluster_center_indices, labels = cluster.affinity_propagation(S, **kwargs)
    return labels

def mean_shift(x, **kwargs):
    """
    NOT scalable, many clusters, uneven cluster size
    Dist between pts.
    """
    clustre_centers, labels = cluster.mean_shift(x, **kwargs)
    return labels

def spectral(x, n, **kwargs):
    """
    Medium n_samples, few clusters, even cluster size
    Graph distance.

    Requires an AFFINITY matrix
    """
    S = np.ones(x.shape) - x
    labels = cluster.spectral_clustering(S, n, **kwargs)
    return labels

def hierarchical(x, n, **kwargs):
    """
    Scalable, many clusters (but with connectivity constraints)
    Play with connectivity settings?  (see sklearn docs)
    """
    ward = cluster.Ward(n_clusters = n, **kwargs).fit(x)
    labels = ward.labels_
    return labels

def DBSCAN(x, eps, min_samples, **kwargs):
    """
    Scalable, uneven cluster sizes
    Distances between NEAREST points
    """
    db = DBSCAN(eps = eps, min_samples = min_samples, **kwargs).fit(x)
    labels = db.labels_
    return labels
