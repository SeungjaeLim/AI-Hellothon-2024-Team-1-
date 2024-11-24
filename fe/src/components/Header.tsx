import SamLogo from "../assets/samLogo.svg?react";
import SsamLogo from "../assets/ssamLogo.svg?react";

interface HeaderProps {
  isSam?: boolean;
  userName?: string;
  userAvatar?: string;
}

function Header({ isSam, userName, userAvatar }: HeaderProps) {
  return (
    <header className="mb-10 flex items-center justify-between">
      {isSam ? <SamLogo /> : <SsamLogo />}
      <div className="flex items-center space-x-2">
        <img src={userAvatar} alt={userName} className="h-8 w-8 rounded-full" />
        <span className="text-lg font-semibold">{userName}</span>
      </div>
    </header>
  );
}

export default Header;
