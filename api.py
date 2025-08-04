import argparse
import app

if __name__ == "__main__":
  emedia_app = app.create_app()
  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--port", type=int, default=5005, help="Port to run the eMedia Face Recognition API on")
  args = parser.parse_args()
  emedia_app.run(host="0.0.0.0", port=args.port)
