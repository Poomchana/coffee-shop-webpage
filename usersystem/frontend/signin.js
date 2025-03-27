function validatePhone() {
    let phoneInput = document.getElementById('phone');
    let phoneError = document.getElementById('phoneError');
    let phoneValue = phoneInput.value;

    // ตรวจสอบว่าทุกตัวอักษรเป็นตัวเลขหรือไม่
    if (!/^\d*$/.test(phoneValue)) {
        phoneError.textContent = 'กรุณากรอกตัวเลขเท่านั้น';
        phoneInput.setCustomValidity('กรุณากรอกตัวเลขเท่านั้น');
    } else {
        // ตรวจสอบความยาวของเบอร์โทรศัพท์
        if (phoneValue.length === 10) {
            phoneError.textContent = '';
            phoneInput.setCustomValidity('');
        } else {
            phoneError.textContent = 'เบอร์โทรศัพท์ต้องมี 10 หลัก';
            phoneInput.setCustomValidity('เบอร์โทรศัพท์ต้องมี 10 หลัก');
        }
    }
}

function validateForm() {
    validatePhone(); // เรียกใช้ฟังก์ชัน validatePhone เพื่อให้แน่ใจว่ามีการตรวจสอบก่อนส่งฟอร์ม
    let phoneInput = document.getElementById('phone');
    return phoneInput.checkValidity(); // ตรวจสอบความถูกต้องของฟอร์ม
}
function checkPassword() {
    let password = document.getElementById("password").value;
    let passwordResult = document.getElementById("passwordResult");
    let result = password.length >= 8 ? "รหัสผ่านปลอดภัย" : "รหัสผ่านสั้นเกินไป";
    passwordResult.innerText = result;
}
function validatePassword() {
    let password = document.getElementById('password').value;
    let confirmPassword = document.getElementById('confirmPassword').value;
    let passwordError = document.getElementById('passwordError');

    if (password !== confirmPassword) {
        passwordError.textContent = 'รหัสผ่านและการยืนยันรหัสผ่านต้องตรงกัน';
    } else {
        passwordError.textContent = '';
    }
}
function validateForm() {
    validatePhone(); // ตรวจสอบเบอร์โทรศัพท์
    validatePassword(); // ตรวจสอบรหัสผ่าน

    let phoneInput = document.getElementById('phone');
    let passwordInput = document.getElementById('password');
    let confirmPasswordInput = document.getElementById('confirmPassword');

    // ตรวจสอบความถูกต้องของฟอร์ม
    if (phoneInput.checkValidity() && passwordInput.value === confirmPasswordInput.value) {
        return true;
    } else {
        return false;
    }
}
