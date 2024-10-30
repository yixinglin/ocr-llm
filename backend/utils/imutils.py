import numpy as np
import faiss
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def faiss_search(query_feature: np.ndarray,
                 feature_list: np.ndarray, k=5) -> list:
    """ This function uses faiss library to search for k nearest neighbors of a query feature in a list of features.

    Args:
        query_feature (_type_): Shape [2048]
        feature_list (_type_): Shape [num_images, 2048]
        k (int, optional): Number of nearest neighbors to search. Defaults to 5.

    Returns:
        _type_: _description_
    """
    d = feature_list.shape[1] # 获取特征向量的维度
    # 建立索引（使用L2距离）特征向量未进行L2归一化
    # faiss_index = faiss.IndexFlatL2(d)
    # 建立FAISS索引（使用内积计算）要先对特征进行L2归一化
    faiss_index = faiss.IndexFlatIP(d)  # Inner Product

    # 添加特征向量到索引 [n, 1024]
    faiss_index.add(feature_list)

    # 为FAISS搜索准备形状为 [1, 2048] 的二维数组
    query_feature = np.array([query_feature]).astype('float32')
    # 搜索最相似的k个向量
    distances, indices = faiss_index.search(query_feature, k)
    # 获取对应的图片路径
    # result_paths = [image_paths[i] for i in indices[0]]  # 返回 k 个最相似的图片路径列表
    # return result_paths, distances[0]  # 返回结果路径列表和对应距离
    return distances[0], indices[0]  # 返回 k 个最相似的图片索引列表
