<?php
/**
 * Optionales Lead-Backend für die FOMO-Marketing-Website.
 *
 * Läuft NUR auf PHP-Hosting (z.B. All-Inkl/Netcup) — NICHT auf GitHub Pages.
 * Auf Pages schlägt der Aufruf fehl und das Formular fällt automatisch auf
 * eine vorausgefüllte WhatsApp-Nachricht zurück (siehe js/main.js).
 *
 * Nimmt den JSON-Submit entgegen und schickt eine Benachrichtigung per Mail.
 * Optional kann hier ein CRM (z.B. Pipedrive) angebunden werden — Token dann
 * per Umgebungsvariable / Datei OBERHALB des Webroots, niemals im Code.
 */
@ini_set('display_errors', '0');
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

function respond($ok, $msg = '') {
  http_response_code($ok ? 200 : 400);
  echo json_encode(array('success' => $ok, 'message' => $msg));
  exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') respond(false, 'Method not allowed');

// ---- Konfiguration ----
// Aktuell gibt es keine Event-E-Mail: Mail-Versand laeuft nur, wenn auf dem
// PHP-Hosting die Umgebungsvariable FOMO_LEAD_EMAIL gesetzt ist.
$TO = getenv('FOMO_LEAD_EMAIL');

$raw = file_get_contents('php://input');
$in = json_decode($raw, true);
if (!is_array($in)) $in = $_POST;
function f($in, $k) { return isset($in[$k]) ? trim((string)$in[$k]) : ''; }

// Honeypot
if (f($in, 'botcheck') !== '') respond(true, 'ok');

$vorname  = f($in, 'vorname');
$nachname = f($in, 'nachname');
$email    = f($in, 'email');
$telefon  = f($in, 'telefon');
$firma    = f($in, 'unternehmen');
$branche  = f($in, 'branche');
$budget   = f($in, 'budget');
$nachricht= f($in, 'nachricht');
$consent  = !empty($in['consent']);

if ($vorname === '' || $nachname === '' || $telefon === '') respond(false, 'Pflichtfelder fehlen');
if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) respond(false, 'E-Mail ungültig');
if (!$consent) respond(false, 'Einwilligung fehlt');
if (preg_match('~https?://|www\.~i', $vorname . ' ' . $nachname)) respond(true, 'ok'); // Spam

$subject = 'FOMO Marketing — Anfrage: ' . $vorname . ' ' . $nachname;
$lines = array(
  'Neue Anfrage über die FOMO-Marketing-Website', '',
  'Name: ' . $vorname . ' ' . $nachname,
  'Telefon: ' . $telefon,
  'E-Mail: ' . ($email !== '' ? $email : '-'),
  'Unternehmen: ' . ($firma !== '' ? $firma : '-'),
  'Branche: ' . ($branche !== '' ? $branche : '-'),
  'Budget: ' . ($budget !== '' ? $budget : '-'),
  'Nachricht: ' . ($nachricht !== '' ? $nachricht : '-'),
);
$body = implode("\n", $lines);
$headers = ($email !== '' ? 'Reply-To: ' . $email . "\r\n" : '') . 'Content-Type: text/plain; charset=utf-8';

if ($TO) @mail($TO, $subject, $body, $headers);

// TODO: optionale CRM-Anbindung hier ergänzen.

respond(true, 'ok');
