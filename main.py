from services.api_service import APIManager

def main():
    api_manager = APIManager()
    # Example usage
    data = api_manager.fetch_data("example_api")
    print(data)

if __name__ == "__main__":
    main()
