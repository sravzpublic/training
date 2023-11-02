use sha2;
use sha2::Sha256;
use sha2::Digest;

pub fn sha256_hash(input: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(input);

    let result = hasher.finalize();
    
    // Convert the result to a hexadecimal string
    let hash_string = result.iter()
        .map(|byte| format!("{:02x}", byte))
        .collect::<String>();

    hash_string
}