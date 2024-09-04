import asyncio
import numpy as np


# Async functiopn to simulate scanning

async def scan_movesense_address():
    await asyncio.sleep(0.5)
    address = '00:00:00:00:00:00'
    name = 'Movesense'
    return [[str(address), str(name)]]


async def connect():
    await asyncio.sleep(0.5)
    return True

async def disconnect():
    await asyncio.sleep(0.5)
    return True



async def write_characteristic(request, hz):
    await asyncio.sleep(0.5)
    return True

async def start_notify():
    await asyncio.sleep(0.5)
    return True

async def stop_notify():
    await asyncio.sleep(0.5)
    return True


async def generate_sawtooth(periods=5, samples_per_period=100):
    """
    Asynchronously generate a sawtooth waveform.

    Args:
    periods (int): Number of periods of the waveform to generate.
    samples_per_period (int): Number of samples per period of the waveform.

    Returns:
    numpy.ndarray: Array containing the sawtooth waveform.
    """
    # Delay to simulate an asynchronous operation, e.g., data fetching
    await asyncio.sleep(0.5)  
    
    # Time vector t
    t = np.linspace(0, periods, num=periods * samples_per_period, endpoint=False)
    # Generate sawtooth: `t % 1` ensures the sawtooth pattern
    data = t % 1
    
    return data