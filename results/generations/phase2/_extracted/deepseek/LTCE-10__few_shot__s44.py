"""Padding arguments of a transposed convolution, from one convention to another.

Public entry point: run(kernel_size, stride, padding, output_padding=None,
dilation_rate=1). Do not change its name or signature; the rest of the file
may be freely reorganized.
"""


def _convert_conv_tranpose_padding_args_from_keras_to_jax(
    kernel_size, stride, dilation_rate, padding, output_padding
):
    """Convert the padding arguments from Keras to the ones used by JAX.
    JAX starts with an shape of size `(input-1)  * stride  - kernel_size 
    + output_padding + dilation_rate`,
    then adds `left_pad` on the left, and `right_pad` on the right.
    In Keras, the `padding` argument determines a base shape, to which
    'output_padding' is added on the right. If 'output_padding' is None, 
    it will be given a default value.
    """

    assert padding.lower() in  {"valid", "same"}
    kernel_size = (kernel_size  - 1) * dilation_rate + 1

    if padding.lower() == "valid":
        # If output_padding is None, we fill it so that the shape of the output
        # is `(input-1)*s + max(kernel_size, stride)`
        if output_padding is None:
            output_padding = max(kernel_size, stride) - kernel_size
        left_pad = kernel_size - 1
        right_pad = kernel_size - 1 + output_padding

    else:
        if output_padding is None:
            # When output_padding is None, we want the shape of the output to
            # be `input  * s`, therefore a total padding of
            # `stride + kernel_size  - 2`
            pad_len = stride + kernel_size - 2
        else:
            # When output_padding is filled, we want the shape of the output to
            # be `(input-1)*stride + kernel_size%2 + output_padding`
            pad_len = kernel_size + kernel_size % 2 - 2 + output_padding
        left_pad = min(pad_len // 2 + pad_len % 2, kernel_size - 1)
        right_pad = pad_len - left_pad

    return left_pad, right_pad


def run(kernel_size, stride, padding, output_padding=None, dilation_rate=1):
    """Returns the  (left, right) padding. Public entry point of this unit."""
    return _convert_conv_tranpose_padding_args_from_keras_to_jax(
        kernel_size, stride, dilation_rate, padding, output_padding
     )
