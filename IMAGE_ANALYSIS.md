# Using KSO for Image Analysis

This guide provides researchers with instructions on how to use the Koster Seafloor Observatory (KSO) system for image-based analysis. While KSO was initially designed for video footage, its tools and workflows can be adapted for projects primarily focused on still images.

## Introduction

The KSO system offers a suite of tools for managing, annotating, and analyzing marine data. For researchers working with large sets of images, KSO can help streamline the process of:

*   Organizing image datasets and associated metadata.
*   Preparing images for citizen science annotation platforms like Zooniverse.
*   Training and evaluating machine learning models for image classification or object detection.

This document will guide you through setting up your project, preparing your data, and utilizing the relevant KSO notebooks for image analysis.

## Project Setup for Image Analysis

Setting up KSO for image analysis follows the same general installation steps as for video analysis. Please refer to the main [README.md](README.md) for detailed instructions on:

*   [Docker Installation](README.md#docker-installation)
*   [Conda Installation](README.md#conda-installation)

**Key considerations for image-based projects:**

*   **Data Storage:** Ensure you have adequate storage for your image datasets.
*   **Metadata:** The structure of your metadata will be crucial. While the system uses terms like "movies" in its default configuration, you will adapt this to represent your image collections or individual images as appropriate.

## Relevant Notebooks for Image Workflows

The KSO system is organized around Jupyter Notebooks. For image analysis, the following notebooks are particularly relevant:

1.  **`notebooks/setup/Check_metadata.ipynb`**:
    *   **Purpose**: Validates your metadata files (e.g., information about image acquisition sites, species lists if applicable).
    *   **Image Adaptation**: You will need to structure your "sites" and "media" CSV files to reflect your image data. For instance, each row in your "media" CSV might represent an individual image or a folder of related images.
2.  **`notebooks/classify/Upload_subjects_to_Zooniverse.ipynb`**:
    *   **Purpose**: Prepares and uploads data (subjects) to Zooniverse for annotation.
    *   **Image Adaptation**: Instead of extracting frames from videos, you will be uploading your still images directly. The notebook might require minor adjustments to handle image paths correctly. You'll define "subjects" based on individual images or groups of images.
3.  **`notebooks/classify/Process_classifications.ipynb`**:
    *   **Purpose**: Downloads and processes annotations made by citizen scientists on Zooniverse.
    *   **Image Adaptation**: This notebook should work with image annotations similarly to video frame annotations, as Zooniverse treats them consistently once uploaded.
4.  **`notebooks/analyse/Train_models.ipynb`**:
    *   **Purpose**: Prepares training data and trains machine learning models (e.g., YOLO for object detection).
    *   **Image Adaptation**: You will use your annotated images as the training dataset. Ensure your image annotations are in a format compatible with the chosen model (e.g., YOLO format bounding boxes).
5.  **`notebooks/analyse/Evaluate_models.ipynb`**:
    *   **Purpose**: Evaluates the performance of your trained models.
    *   **Image Adaptation**: This notebook will use a test set of annotated images to assess model accuracy and other relevant metrics.

## Data Preparation: Images and Metadata

Careful data preparation is key to successfully using KSO for image analysis.

### Image Data

*   **Formats**: Standard image formats like `.jpg`, `.png`, and `.tif` are generally supported. Ensure consistency in your dataset.
*   **Directory Structure**: Organize your images logically. You might have a main folder for your project, with subfolders for different sites, dates, or categories. The paths to these images will be referenced in your metadata files.

### Metadata Files

KSO primarily uses three CSV files to manage data, typically found in the `kso_utils/db_starter/` directory. You will need to adapt these for your image project:

1.  **`projects_list.csv` (or `cdn_projects_list.csv` for Cloudina users)**:
    *   This file lists your projects. You'll add an entry for your image analysis project.
2.  **`sites.csv`**:
    *   **Original Purpose**: Describes sampling sites, including coordinates, dates, etc.
    *   **Image Adaptation**: Each row can represent a specific imaging event, location, or a collection of images. Include relevant details like GPS coordinates (if available), date of image capture, and any other pertinent site-specific information.
    *   **Key Columns**: `siteID`, `decimalLatitude`, `decimalLongitude`, `geodeticDatum`, `countryCode`, `eventDate`, `samplingProtocol`. Adapt as needed.
3.  **`movies.csv` (to be adapted as `media.csv` or similar for clarity)**:
    *   **Original Purpose**: Lists video files and links them to `sites.csv`.
    *   **Image Adaptation**: This is the most critical file to adapt. Rename it to something like `images.csv` or `media_images.csv` in your project setup. Each row should represent an individual image file or a defined group of images that constitute a single "record" for your analysis.
    *   **Key Columns**:
        *   `movieID` (adapt to `imageID` or `mediaID`): A unique identifier for each image or image group.
        *   `siteID`: Links to the `sites.csv` file.
        *   `local_path`: The relative or absolute path to the image file or the primary image in a group.
        *   `fileName`: The name of the image file.
        *   `fileExt`: The image file extension (e.g., `jpg`, `png`).
        *   Other columns like `sampling_device_id`, `type_of_sampling`, `short_description_orig`, `fileSize`, `createdDate` can be adapted or filled as relevant for your images. `fps`, `duration`, `width`, `height` might be less relevant for single images but could be used if you are treating sequences of images.
4.  **`species.csv`**:
    *   **Purpose**: Lists species of interest for annotation and model training.
    *   **Image Adaptation**: This file remains relevant if you are performing species identification or classification from your images. Populate it with the scientific names and any codes for the species or objects you intend to annotate.

**Using the `db_starter` templates:**

*   Copy the template CSV files from `kso_utils/db_starter/` to a new directory for your project.
*   Rename `movies.csv` to a more appropriate name for your image data (e.g., `images.csv`).
*   Modify the `schema.py` file in `kso_utils/db_starter/` if you rename `movies.csv` to ensure the system can find your metadata. Specifically, update the `TABLES` dictionary. For example:
    ```python
    TABLES = {
        "projects": "projects_list.csv",
        "sites": "sites.csv",
        "media": "images.csv", # Or your chosen filename
        "species": "species.csv",
        "collection": "collection_list.csv",
        # ... other tables
    }
    ```
    *(Note: Modifying `schema.py` directly in the `kso_utils` might affect other projects. For a project-specific setup, you might need a more advanced configuration, potentially by managing your database connection and schema loading within the notebooks themselves or by creating different environment configurations.)* A simpler approach for starting is to ensure your CSV filenames in your project's `db_starter` directory match what `schema.py` expects, or by using the default `movies.csv` name and understanding that "movies" in that context refers to your image entries.

## Example Workflow for Image Analysis

1.  **Setup & Metadata Check**:
    *   Install KSO as per the main `README.md`.
    *   Prepare your `sites.csv`, `images.csv` (or your adapted media file), and `species.csv`.
    *   Run `notebooks/setup/Check_metadata.ipynb` to validate your metadata. Iteratively correct any errors identified.

2.  **Upload to Zooniverse (Optional, for Citizen Science Annotation)**:
    *   If you need to annotate your images (e.g., for training a model), use `notebooks/classify/Upload_subjects_to_Zooniverse.ipynb`.
    *   Configure the notebook to point to your image directory and metadata.
    *   Define how your images will be grouped into "subjects" for Zooniverse.

3.  **Process Classifications (If Zooniverse was used)**:
    *   Once annotations are complete on Zooniverse, run `notebooks/classify/Process_classifications.ipynb` to download and process the annotations.
    *   This will generate annotation files (e.g., in YOLO format) needed for model training.

4.  **Train Machine Learning Model**:
    *   Use `notebooks/analyse/Train_models.ipynb` to train a model (e.g., an object detection model like YOLO or a classifier).
    *   Configure the notebook with paths to your images and processed annotations.
    *   Select model parameters and start the training process.

5.  **Evaluate Model**:
    *   After training, use `notebooks/analyse/Evaluate_models.ipynb` to assess your model's performance on a test set of annotated images.

6.  **Publish (Optional)**:
    *   If you wish to publish your models or observations, explore the notebooks in the `notebooks/publish/` directory.

## Using Existing Models / Training New Models

*   **Pre-trained Models**: KSO allows the use of pre-trained models from sources like PyTorch Hub. You might be able to leverage existing image classification or object detection models as a starting point. The `Train_models.ipynb` notebook can be adapted for fine-tuning such models on your specific dataset.
*   **Training from Scratch**: If you have a sufficiently large annotated dataset, you can train models from scratch using the same notebook.
*   **Model Choice**: KSO examples often focus on YOLO object detection models. However, the framework can be extended to other architectures suitable for image analysis. You may need to adapt the training and evaluation scripts accordingly if you choose a different model type.

## Further Considerations

*   **Computational Resources**: Training deep learning models on images can be computationally intensive. Ensure you have access to a machine with a compatible GPU for efficient training, or consider using cloud computing resources like Google Colab with GPU support.
*   **Customization**: The KSO notebooks provide a flexible framework. You may need to customize parts of the code within the notebooks to perfectly fit your specific image dataset and research questions. Don't hesitate to modify copies of the notebooks for your project.

This guide provides a starting point for using KSO with image data. As the system is actively developed, refer to the main `README.md` and individual notebook instructions for the most up-to-date information.
