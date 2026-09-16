import kagglehub

# Download latest version
path = kagglehub.dataset_download("wikimedia-foundation/wikipedia-structured-contents")

print("Path to dataset files:", path)
