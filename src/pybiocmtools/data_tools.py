import anndata
from scipy import io
import numpy as np
import os
import pandas as pd

def load_anndata(args):
    # load sparse matrix:
    print(f"Loading data from {args.input}")
    print(f"Loading counts matrix...")
    X = io.mmread(os.path.join(args.input, "counts.mtx"))

    print(f"Creating AnnData object...")
    # create anndata object
    adata = anndata.AnnData(
        X=X.transpose().tocsr(),
        dtype=X.dtype
    )

    # load cell metadata:
    print(f"Loading metadata...")
    cell_meta = pd.read_csv(os.path.join(args.input, "metadata.csv"))

    # load gene names
    print(f"Loading gene names...")
    with open(os.path.join(args.input, "gene_names.csv"), 'r') as f:
        gene_names = f.read().splitlines()

    # set anndata observations and index obs by barcodes, var by gene names
    adata.obs = cell_meta
    adata.obs.index = adata.obs['barcode']
    adata.var.index = gene_names

    # load dimensional reduction:
    print(f"Loading pca...")
    pca = pd.read_csv(os.path.join(args.input, "pca.csv"), index_col=[0])
    pca.index = adata.obs.index
    adata.obsm['X_pca'] = pca.to_numpy()

    if "harmony.csv" in os.listdir():
        print("harmony.csv detected, loading harmony reduction...")
        harmony = pd.read_csv(os.path.join(args.input, "harmony.csv"), index_col=[0])
        harmony.index = adata.obs.index
        adata.obsm['X_harmony'] = harmony.to_numpy()

    # set pca and umap
    print(f"Loading umap...")
    adata.obsm['X_umap'] = np.vstack((adata.obs['UMAP_1'].to_numpy(), adata.obs['UMAP_2'].to_numpy())).T

    # save dataset as anndata format
    print(f"Saving AnnData object to: {args.output}")
    adata.write(args.output)


if __name__ == "__main__":
    # setting the parameters
    import argparse

    parser = argparse.ArgumentParser(description='Create Anndata file from prepared Seurat directory',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', default=None, required=True)
    parser.add_argument('--output', default='anndata.h5ad')

    args = parser.parse_args()

    load_anndata(args)