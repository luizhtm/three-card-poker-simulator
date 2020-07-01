import random
import math
import multiprocessing

def generate_deck():
	cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
	colors = ['D', 'C', 'S', 'H']
	deck = []
	for card in cards:
		for color in colors:
			deck.append('{card}{color}'.format(card=card, color=color))

	return deck

def distribute_hand(deck):
	card_1 = deck.pop()
	card_2 = deck.pop()
	card_3 = deck.pop()

	hand = [card_1, card_2, card_3]

	return deck, hand

def check_hand(hand):
	rankings = {
		'2': 2,
		'3': 3,
		'4': 4,
		'5': 5,
		'6': 6,
		'7': 7,
		'8': 8,
		'9': 9,
		'T': 10,
		'J': 11,
		'Q': 12,
		'K': 13,
		'A': 14
	}

	sorted_hand = sorted(hand, key=lambda card: rankings[card[0]])

	# print(sorted_hand)

	card_1 = sorted_hand[0]
	card_2 = sorted_hand[1]
	card_3 = sorted_hand[2]

	straight = rankings[card_3[0]] == rankings[card_2[0]] + 1 and rankings[card_2[0]] == rankings[card_1[0]] + 1
	three_of_a_kind = card_1[0] == card_2[0] == card_3[0]
	flush = card_1[1] == card_2[1] == card_3[1]
	pair = card_1[0] == card_2[0] or card_2[0] == card_3[0]

	base_score = rankings[card_3[0]]
	if straight and flush:
		return 100000000000000 * base_score
	if three_of_a_kind:
		return 1000000000000 * base_score
	if straight:
		return 10000000000 * base_score
	if flush:
		return 100000000 * base_score
	if pair:
		base_score = rankings[card_2[0]]
		if rankings[card_3[0]] != rankings[card_2[0]]:
			return (1000000 * base_score) + rankings[card_3[0]]
		else:
			return (1000000 * base_score) + rankings[card_1[0]]

	base_score = (10000 * rankings[card_3[0]]) + (100 * rankings[card_2[0]]) + (1 * rankings[card_1[0]])
	return base_score

def play_single_game(i):	
	deck = generate_deck()
	random.shuffle(deck)

	deck, player_hand = distribute_hand(deck)
	player_score = check_hand(player_hand)

	# Assuming player is playing optimal strategy, which is playing Q 6 4 or higher.
	if player_score < 120604:
		return 'fold'

	deck, dealer_hand = distribute_hand(deck)
	dealer_score = check_hand(dealer_hand)

	if dealer_score < 120000:
		return 'not qualified'
	else:
		if player_score > dealer_score:
			return 'wins'
		elif player_score == dealer_score:
			return 'push'
		else:
			return 'lose'
	

if __name__ == '__main__':
	balance = 100000
	n_of_games = 100000
	bet = 1

	print("Starting balance is: ${balance}".format(balance=balance))
	print("Number of games: {n_of_games}".format(n_of_games=n_of_games))

	# Cria uma 'pool' com o número de threads que tem na máquina.
	pool = multiprocessing.Pool(multiprocessing.cpu_count())

	# Faz cada uma das cpus executarem um jogo, 
	# e o resultado de cada jogo é guardado no vetor results.
	results = pool.map(play_single_game, range(n_of_games))

	# Fecha a pool
	pool.close()

	# Verifica cada resultado de maneira serial e contabiliza os resultados dos jogos.
	for result in results:
		if result == 'fold':
			balance -= bet
		elif result == 'not qualified':
			balance += bet
		elif result == 'wins':
			balance += 2 * bet
		elif result == 'push':
			pass
		else:
			balance -= 2 * bet

	print("\nFinal balance is ${balance}".format(balance=balance))