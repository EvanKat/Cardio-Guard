
# Cardio-Guard
**An AI-Driven Cardiovascular Monitoring and Arrhythmia Detection System**

A proposed project on heart monitoring for my thesis at the ECE Department, Technical University of Crete.

---

## Getting Started

### Installation
First, install the necessary dependencies by running:

```bash
pip install -r requirements.txt
```

### Usage

1. **Connect to a Movesense Device and Capture ECG Data**  
   To connect to a Movesense device, capture raw ECG data, and process it, run:

   ```bash
   python manage.py
   ```

2. **Display Processed Data**  
   To display the processed data, use:

   ```bash
   python analytics.py
   ```

### Troubleshooting

- **No Movesense Device Available?**  
  If a Movesense device is not available, and you need to run `manage.py`, modify the code as follows:
  - **Uncomment** the `hl.*` methods.
  - **Comment** the referring `mv_blk.*` methods.

### Limitations

- Currently, the `manage.py` application can only connect to one Movesense device and process ECG data.
- The application might be a bit buggy at times, so please report any issues encountered.

---

## TODO
- Update the project documentation and improve stability.
