use tokio::time::{sleep, Duration};
use futures::Future;

/// Execute a Time-Weighted Average Price order slicing.
/// `order_size` is total size, `duration` total time to spread across.
/// `send` is a callback used to submit each sliced order.
pub async fn twap_slice<F, Fut>(order_size: f64, duration: Duration, mut send: F)
where
    F: FnMut(f64) -> Fut,
    Fut: Future<Output = ()> + Send,
{
    let slices = 10u32;
    let slice_size = order_size / slices as f64;
    let interval = duration / slices;
    for _ in 0..slices {
        send(slice_size).await;
        sleep(interval).await;
    }
}
