import tritonclient.grpc.aio as grpcclient
import tritonclient.http as httpclient
import tritonclient.http.aio as ahttpclient
from loguru import logger
from tritonclient import http


def get_triton_grpc_client(url: str = "localhost:8001"):
    try:
        keepalive_options = grpcclient.KeepAliveOptions(
            keepalive_time_ms=2**31 - 1,
            keepalive_timeout_ms=20000,
            keepalive_permit_without_calls=False,
            http2_max_pings_without_data=2,
        )
        triton_grpc_client = grpcclient.InferenceServerClient(
            url=url, verbose=False, keepalive_options=keepalive_options
        )
    except Exception as e:
        logger.error(f"Nvidia triton inference server channel creation failed: {e}")
        return None
    return triton_grpc_client


async def get_triton_http_client(url: str = "localhost:8000"):
    try:
        triton_http_client = ahttpclient.InferenceServerClient(url=url, verbose=False)
    except Exception as e:
        logger.error(f"Nvidia triton inference server channel creation failed: {e}")
        return None
    return triton_http_client


def get_triton_http_client_sync(url: str = "localhost:8000"):
    try:
        triton_http_client = httpclient.InferenceServerClient(url=url, verbose=False)
    except Exception as e:
        logger.error(f"Nvidia triton inference server channel creation failed: {e}")
        return None
    return triton_http_client


def is_triton_server_ready(url: str = "localhost:8000", model_name: str = ""):
    try:
        triton_http_client = http.InferenceServerClient(
            url=url, verbose=False, connection_timeout=5, network_timeout=5
        )
        if not triton_http_client.is_server_ready():
            logger.warning(f"Triton server at {url} is not ready")
            return False
        if model_name != "" and not triton_http_client.is_model_ready(
            model_name=model_name
        ):
            logger.warning(
                f"Model {model_name} is not ready on the Triton server at {url}"
            )
            return False
    except Exception as e:
        logger.error(f"Error checking model readiness: {e}")
        return False
    return True


if __name__ == "__main__":
    print(is_triton_server_ready(url="192.168.0.16:4060", model_name="kokoro-model"))
