import { Link } from "@tanstack/react-router";

interface TabItem {
  id: string;
  title?: string;
  subtitle?: string;
  path?: string;
}

interface TabsProps {
  title?: string;
  subtitle?: string;
  activeTab: string;
  items: TabItem[];
}

function Tabs({ title, subtitle, activeTab, items }: TabsProps) {
  return (
    <div className="flex flex-col items-center justify-center gap-3">
      {title && (
        <div>
          <span className="text-2xl font-semibold leading-loose">{title}</span>
          <span className="text-lg font-semibold leading-loose">
            {subtitle}
          </span>
        </div>
      )}
      <div className="inline-flex items-center justify-start self-stretch">
        {items.map((item) => (
          <div
            key={item.id}
            className={`shrink grow basis-0 p-2 ${
              activeTab == item.id
                ? "border-b-2 border-black-13"
                : "border-b-2 border-black-1"
            } flex items-center justify-center`}
          >
            {item.path ? (
              <Link to={item.path} className="text-center">
                <span
                  className={`${
                    activeTab == item.id ? "" : "text-black-7"
                  } text-base font-semibold leading-relaxed`}
                >
                  {item.title}
                  <br />
                </span>
                {item.subtitle && (
                  <span
                    className={`${
                      activeTab == item.id ? "" : "text-black-7"
                    } text-base font-medium leading-relaxed`}
                  >
                    {item.subtitle}
                  </span>
                )}
              </Link>
            ) : (
              <>
                <span
                  className={`${
                    activeTab === item.id ? "" : "text-black-7"
                  } text-base font-semibold leading-relaxed`}
                >
                  {item.title}
                  <br />
                </span>
                {item.subtitle && (
                  <span
                    className={`${
                      activeTab === item.id ? "" : "text-black-7"
                    } text-base font-medium leading-relaxed`}
                  >
                    {item.subtitle}
                  </span>
                )}
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Tabs;
