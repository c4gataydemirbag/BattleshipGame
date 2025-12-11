using Microsoft.AspNetCore.SignalR;
using System.Collections.Concurrent;

public class GameHub : Hub
{
	// Oyuncuları tutan liste (Static olduğu için hafızada kalır)
	private static ConcurrentDictionary<string, string> Players = new ConcurrentDictionary<string, string>();
	// Player1 -> ConnectionID
	// Player2 -> ConnectionID

	public override async Task OnConnectedAsync()
	{
		string role = "";

		// İçeride kaç kişi var?
		if (!Players.ContainsKey("Player1"))
		{
			role = "Player1";
			Players.TryAdd("Player1", Context.ConnectionId);
		}
		else if (!Players.ContainsKey("Player2"))
		{
			role = "Player2";
			Players.TryAdd("Player2", Context.ConnectionId);
		}
		else
		{
			// 3. kişi gelirse oyuna almayalım veya izleyici olsun
			await Clients.Caller.SendAsync("Hata", "Oda Dolu!");
			return;
		}

		// Oyuncuya rolünü bildir
		await Clients.Caller.SendAsync("RolAtandi", role);

		// Eğer Player2 de geldiyse Player1'e haber ver "Rakip Geldi" diye
		if (role == "Player2")
		{
			string p1Id = Players["Player1"];
			await Clients.Client(p1Id).SendAsync("RakipBaglandi"); // P1'e haber ver
			await Clients.Caller.SendAsync("RakipBaglandi");       // P2'ye (kendine) haber ver
		}

		await base.OnConnectedAsync();
	}

	// --- OYUN METODLARI ---

	// Artık parametre olarak isim almaya gerek yok, kimin attığını ID'den bulacağız
	public async Task AtesEt(int x, int y)
	{
		string myId = Context.ConnectionId;
		string myRole = Players.FirstOrDefault(x => x.Value == myId).Key;
		string targetRole = (myRole == "Player1") ? "Player2" : "Player1";

		if (Players.TryGetValue(targetRole, out string targetId))
		{
			await Clients.Client(targetId).SendAsync("SaldiriGeldi", x, y);
		}
	}

	public async Task SonucBildir(int x, int y, bool isHit)
	{
		string myId = Context.ConnectionId;
		string myRole = Players.FirstOrDefault(x => x.Value == myId).Key;
		string targetRole = (myRole == "Player1") ? "Player2" : "Player1";

		if (Players.TryGetValue(targetRole, out string targetId))
		{
			await Clients.Client(targetId).SendAsync("SonucGeldi", x, y, isHit);
		}
	}

	public async Task Hazirim()
	{
		string myId = Context.ConnectionId;
		string myRole = Players.FirstOrDefault(x => x.Value == myId).Key;
		string targetRole = (myRole == "Player1") ? "Player2" : "Player1";

		if (Players.TryGetValue(targetRole, out string targetId))
		{
			await Clients.Client(targetId).SendAsync("RakipHazir");
		}
	}

	public async Task OyunBitti(string kazanan)
	{
		await Clients.All.SendAsync("OyunBitti", kazanan);
	}

	// Bağlantı koparsa listeyi temizle (Basitlik için)
	public override async Task OnDisconnectedAsync(Exception? exception)
	{
		string myId = Context.ConnectionId;
		var item = Players.FirstOrDefault(kvp => kvp.Value == myId);
		if (!string.IsNullOrEmpty(item.Key))
		{
			Players.TryRemove(item.Key, out _);
		}
		await base.OnDisconnectedAsync(exception);
	}
}