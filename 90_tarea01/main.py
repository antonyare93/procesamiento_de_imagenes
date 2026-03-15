def main():
    from supervision.assets import download_assets, VideoAssets

    download_assets(VideoAssets.VEHICLES)
    "vehicles.mp4"


if __name__ == "__main__":
    main()
