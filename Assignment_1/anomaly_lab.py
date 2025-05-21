import random
from statistics import mean, stdev

def flag_anomalies(amounts: list[int], student_id: str) -> list[int]:
	# Flags repayments whose distance from μ exceeds 1.5·σ of a 10 % random sample.
	# A student-specific seed (last 3 ID digits) personalises the result.
	# 1️⃣ Personalised seed -------------------------------------------------
	random.seed(int(student_id[-3:]))
	# 2️⃣ Tiny sample (10 % of the data; never less than 1 item) ------------
	sample = random.sample(amounts, k=max(1, len(amounts) // 10))
	# 3️⃣ Statistical threshold --------------------------------------------
	μ = mean(sample)
	σ = stdev(sample) if len(sample) > 1 else 0 # σ=0 if sample size = 1
	# 4️⃣ Flag anomalies -----------------------------------------------------
	return [a for a in amounts if abs(a - μ) > 1.5 * σ]

# --------------------------------------------------------------------------
transactions = [102, 98, 97, 99, 101, 100, 250,
				97, 95, 420, 101, 99]
result = flag_anomalies(transactions, student_id="8991 782") # ← replace with YOUR ID
print(result)
