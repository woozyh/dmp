from src.cosineSimilarity import CosineSimilarity

def main():
    cosine = CosineSimilarity()
    cosine.cosineSimilarityAndDistance()
    cosine.dataToCsv(cosine.cosineDis, "cosineDis")
    cosine.dataToCsv(cosine.cosineSim, "cosineSim")

if __name__ == "__main__":
    main()