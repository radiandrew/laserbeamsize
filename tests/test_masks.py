import numpy as np
import laserbeamsize

np.set_printoptions(threshold=np.inf)

# Sample image
image = np.zeros((100, 100))

################ elliptical_mask()

def test_elliptical_mask():
    mask = laserbeamsize.elliptical_mask(image, 50, 50, 40, 20, np.pi/4)
    assert mask.shape == image.shape, "Mask shape mismatch"

def test_elliptical_mask_same_shape():
    mask = laserbeamsize.elliptical_mask(image, 50, 50, 40, 60, 0)
    assert mask.shape == image.shape, "Output mask shape mismatch with input image shape."

def test_elliptical_mask_unrotated():
    mask = laserbeamsize.elliptical_mask(image, 50, 50, 40, 60, 0)
    assert not np.any(mask[:20, :])
    assert not np.any(mask[81:, :])
    assert not np.any(mask[:, :15])
    assert not np.any(mask[:,81 :])
    assert np.all(mask[50,30:70])
    assert np.all(mask[20:80, 50])

def test_elliptical_mask_rotated():
    mask = laserbeamsize.elliptical_mask(image, 50, 50, 40, 60, np.pi/4)  # 45-degree rotation
    unrotated_mask = laserbeamsize.elliptical_mask(image, 50, 50, 40, 60, 0)
    assert not np.array_equal(mask, unrotated_mask), "Rotated mask should not be the same as the unrotated one."

def test_elliptical_mask_edge_cases():
    mask = laserbeamsize.elliptical_mask(image, 150, 150, 200, 200, 0)
    assert mask.shape == image.shape, "Output mask shape mismatch with input image shape for edge cases."

################ corner_mask()
def test_corner_mask():
    mask = laserbeamsize.corner_mask(image)
    assert mask.shape == image.shape, "Mask shape mismatch"
    # You can check corners of the mask here.

def test_corner_mask_default_fraction():
    mask = laserbeamsize.corner_mask(image)
    total_pixels = image.size
    expected_true_pixels = 4 * (int(0.035 * 100))**2  # for a 100x100 image
    assert np.sum(mask) == expected_true_pixels, f"Expected {expected_true_pixels} True pixels, but got {np.sum(mask)}."

def test_corner_mask_custom_fraction():
    custom_fraction = 0.05  # 5%
    mask = laserbeamsize.corner_mask(image, corner_fraction=custom_fraction)
    total_pixels = image.size
    expected_true_pixels = 4 * (custom_fraction * 100)**2
    assert np.sum(mask) == expected_true_pixels, f"Expected {expected_true_pixels} True pixels, but got {np.sum(mask)}."

def test_corner_mask_large_image():
    large_image = np.zeros((1000, 1000))
    mask = laserbeamsize.corner_mask(large_image)
    assert mask.shape == large_image.shape, "Mask shape mismatch with large image"

def test_mask_regions_are_correct():
    mask = laserbeamsize.corner_mask(image)
    n, m = int(100 * 0.035), int(100 * 0.035)  # for a 100x100 image with default fraction
    # Ensure center of the mask is False
    assert not np.any(mask[n:-n, m:-m]), "Center of the mask should be False"
    # Ensure corners are True
    assert np.all(mask[:n, :m])
    assert np.all(mask[:n, -m:])
    assert np.all(mask[-n:, :m])
    assert np.all(mask[-n:, -m:])

################ perimeter_mask()

def test_perimeter_mask():
    mask = laserbeamsize.perimeter_mask(image)
    assert mask.shape == image.shape, "Mask shape mismatch"
    # You can check the perimeter of the mask here.

def test_perimeter_mask_basic():
    result = laserbeamsize.perimeter_mask(image)
    assert np.all(result[:3, :] == True)
    assert np.all(result[-3:, :] == True)
    assert np.all(result[:, :3] == True)
    assert np.all(result[:, -3:] == True)
    assert np.all(result[4:-4, 4:-4] == False)

def test_perimeter_mask_fraction():
    result = laserbeamsize.perimeter_mask(image, corner_fraction=0.1)
    assert np.all(result[:9, :] == True)
    assert np.all(result[-9:, :] == True)
    assert np.all(result[:, :9] == True)
    assert np.all(result[:, -9:] == True)
    assert np.all(result[10:-10, 10:-10] == False)

def test_perimeter_mask_odd_dimension():
    image2 = np.zeros((101, 101), dtype=bool)
    result = laserbeamsize.perimeter_mask(image2)
    assert np.all(result[:3, :] == True)
    assert np.all(result[-3:, :] == True)
    assert np.all(result[:, :3] == True)
    assert np.all(result[:, -3:] == True)
    assert np.all(result[4:-4, 4:-4] == False)

def test_perimeter_mask_non_square():
    image2 = np.zeros((150, 50), dtype=bool)
    result = laserbeamsize.perimeter_mask(image2)
    assert np.all(result[:5, :] == True)  # 0.035*150 ~ 5.25 which rounds to 6
    assert np.all(result[-5:, :] == True)
    assert np.all(result[:, :1] == True)  # 0.035*50 ~ 1.75 which rounds to 2
    assert np.all(result[:, -1:] == True)
    assert np.all(result[6:-6, 2:-2] == False)

################ rotated_rect_mask_slow()

def test_rotated_rect_mask_slow():
    mask = laserbeamsize.masks.rotated_rect_mask_slow(image, 50, 50, 40, 20, np.pi/4)
    assert mask.shape == image.shape, "Mask shape mismatch"

def test_rotated_rect_mask():
    mask = laserbeamsize.rotated_rect_mask(image, 50, 50, 40, 20, np.pi/4)
    assert mask.shape == image.shape, "Mask shape mismatch"

# def test_basic_comparison():
#     image = np.zeros((100, 100), dtype=bool)
#     mask_fast = laserbeamsize.rotated_rect_mask(image, 50, 50, 20, 30, np.pi/6)
#     mask_slow = laserbeamsize.masks.rotated_rect_mask_slow(image, 50, 50, 20, 30, np.pi/6)
#     assert np.array_equal(mask_fast, mask_slow)
# 
# def test_varying_dimensions():
#     image = np.zeros((150, 150), dtype=bool)
#     mask_fast = laserbeamsize.rotated_rect_mask(image, 75, 75, 30, 60, np.pi/4)
#     mask_slow = laserbeamsize.masks.rotated_rect_mask_slow(image, 75, 75, 30, 60, np.pi/4)
#     assert np.array_equal(mask_fast, mask_slow)
# 
# def test_varying_rotation():
#     image = np.zeros((200, 200), dtype=bool)
#     mask_fast = laserbeamsize.rotated_rect_mask(image, 100, 100, 40, 60, np.pi/3)
#     mask_slow = laserbeamsize.masks.rotated_rect_mask_slow(image, 100, 100, 40, 60, np.pi/3)
#     assert np.array_equal(mask_fast, mask_slow)
# 
# def test_off_center():
#     image = np.zeros((250, 250), dtype=bool)
#     mask_fast = laserbeamsize.rotated_rect_mask(image, 60, 190, 50, 70, np.pi/2)
#     mask_slow = laserbeamsize.masks.rotated_rect_mask_slow(image, 60, 190, 50, 70, np.pi/2)
#     assert np.array_equal(mask_fast, mask_slow)

if __name__ == "__main__":
    test_elliptical_mask()
    test_elliptical_mask_same_shape()
    test_elliptical_mask_unrotated()
    test_elliptical_mask_rotated()
    test_elliptical_mask_edge_cases()

    test_corner_mask()
    test_corner_mask_default_fraction()
    test_corner_mask_custom_fraction()
    test_corner_mask_large_image()
    test_mask_regions_are_correct()

    test_perimeter_mask()
    test_perimeter_mask_basic()
    test_perimeter_mask_fraction()
    test_perimeter_mask_odd_dimension()
    test_perimeter_mask_non_square()

    test_rotated_rect_mask_slow()
    test_rotated_rect_mask()
    print("All tests passed!")

if __name__ == "__main__":
    # ... [other tests]


    print("All tests passed!")

